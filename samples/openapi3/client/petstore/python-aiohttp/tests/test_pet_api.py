# coding: utf-8

# flake8: noqa

"""
Run the tests.
$ docker pull swaggerapi/petstore
$ docker run -d -e SWAGGER_HOST=http://petstore.swagger.io -e SWAGGER_BASE_PATH=/v2 -p 80:8080 swaggerapi/petstore
$ pytest -vv
"""

import os
import sys
import unittest
import asyncio
import pytest
import aiohttp

import petstore_api
from petstore_api import Configuration
from petstore_api.rest import ApiException

from .util import id_gen, async_test

import json

import urllib3

HOST = 'http://localhost:80/v2'


class TestPetApiTests(unittest.TestCase):

    def setUp(self):
        config = Configuration()
        config.host = HOST

        self.api_client = petstore_api.ApiClient(config)
        self.pet_api = petstore_api.PetApi(self.api_client)
        self.setUpModels()
        self.setUpFiles()

    def setUpModels(self):
        self.category = petstore_api.Category(id=id_gen(), name="dog")
        #self.category.id = id_gen()
        #self.category.name = "dog"
        self.tag = petstore_api.Tag()
        self.tag.id = id_gen()
        self.tag.name = "openapi-generator-python-pet-tag"
        self.pet = petstore_api.Pet(name="hello kity", photoUrls=["http://foo.bar.com/1", "http://foo.bar.com/2"])
        self.pet.id = id_gen()
        self.pet.status = "sold"
        self.pet.category = self.category
        self.pet.tags = [self.tag]

    def setUpFiles(self):
        self.test_file_dir = os.path.join(os.path.dirname(__file__), "..", "testfiles")
        self.test_file_dir = os.path.realpath(self.test_file_dir)
        self.foo = os.path.join(self.test_file_dir, "foo.png")

    def test_separate_default_client_instances(self):
        pet_api = petstore_api.PetApi()
        pet_api2 = petstore_api.PetApi()
        self.assertEqual(id(pet_api.api_client), id(pet_api2.api_client))

    def test_separate_default_config_instances(self):
        pet_api = petstore_api.PetApi()
        pet_api2 = petstore_api.PetApi()
        self.assertEqual(id(pet_api.api_client.configuration), id(pet_api2.api_client.configuration))

    @async_test
    async def test_async_with_result(self):
        await self.pet_api.add_pet(self.pet)

        tasks = [
            asyncio.create_task(coro)
            for coro in [
                self.pet_api.get_pet_by_id(self.pet.id),
                self.pet_api.get_pet_by_id(self.pet.id),
            ]
        ]

        responses = await asyncio.gather(*tasks)
        for response in responses:
            self.assertEqual(response.id, self.pet.id)
        self.assertEqual(len(responses), 2)

    @async_test
    async def test_exception(self):
        await self.pet_api.add_pet(self.pet)

        try:
            await self.pet_api.get_pet_by_id(9999999999999)
        except ApiException as e:
            exception = e

        self.assertIsInstance(exception, ApiException)
        self.assertEqual(exception.status, 404)

    @async_test
    async def test_add_pet_and_get_pet_by_id(self):
        await self.pet_api.add_pet(self.pet)

        fetched = await self.pet_api.get_pet_by_id(pet_id=self.pet.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(self.pet.id, fetched.id)
        self.assertIsNotNone(fetched.category)
        self.assertEqual(self.pet.category.name, fetched.category.name)

    @async_test
    async def test_add_pet_and_get_pet_by_id_with_http_info(self):
        await self.pet_api.add_pet(self.pet)

        fetched = await self.pet_api.get_pet_by_id_with_http_info(pet_id=self.pet.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(self.pet.id, fetched.data.id)
        self.assertIsNotNone(fetched.data.category)
        self.assertEqual(self.pet.category.name, fetched.data.category.name)

    @async_test
    async def test_add_pet_and_get_pet_by_id_without_preload_content(self):
        await self.pet_api.add_pet(self.pet)

        fetched = await self.pet_api.get_pet_by_id_without_preload_content(pet_id=self.pet.id)
        self.assertIsInstance(fetched, aiohttp.ClientResponse)
        # self.assertFalse(fetched.closed)
        # self.assertFalse(fetched.content._eof)
        read = await fetched.content.read()
        self.assertTrue(fetched.closed)
        self.assertTrue(fetched.content._eof)
        self.assertIsInstance(read, bytes)
        self.assertEqual(await fetched.content.read(), b'')
        self.assertTrue(read.decode("utf-8").startswith('{"id":'))

    @async_test
    async def test_update_pet(self):
        self.pet.name = "hello kity with updated"
        await self.pet_api.update_pet(self.pet)

        fetched = await self.pet_api.get_pet_by_id(pet_id=self.pet.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(self.pet.id, fetched.id)
        self.assertEqual(self.pet.name, fetched.name)
        self.assertIsNotNone(fetched.category)
        self.assertEqual(fetched.category.name, self.pet.category.name)

    @async_test
    async def test_find_pets_by_status(self):
        await self.pet_api.add_pet(self.pet)
        pets = await self.pet_api.find_pets_by_status(status=[self.pet.status])
        self.assertIn(
            self.pet.id,
            list(map(lambda x: getattr(x, 'id'), pets))
        )

    @async_test
    async def test_find_pets_by_tags(self):
        await self.pet_api.add_pet(self.pet)
        pets = await self.pet_api.find_pets_by_tags(tags=[self.tag.name])
        self.assertIn(
            self.pet.id,
            list(map(lambda x: getattr(x, 'id'), pets))
        )

    @async_test
    async def test_update_pet_with_form(self):
        await self.pet_api.add_pet(self.pet)

        name = "hello kity with form updated"
        status = "pending"
        await self.pet_api.update_pet_with_form(pet_id=self.pet.id, name=name, status=status)

        fetched = await self.pet_api.get_pet_by_id(pet_id=self.pet.id)
        self.assertEqual(self.pet.id, fetched.id)
        self.assertEqual(name, fetched.name)
        self.assertEqual(status, fetched.status)

    @async_test
    async def test_upload_file(self):
        # upload file with form parameter
        try:
            additional_metadata = "special"
            await self.pet_api.upload_file(
                pet_id=self.pet.id,
                additional_metadata=additional_metadata,
                file=self.foo
            )
        except ApiException as e:
            self.fail("upload_file() raised {0} unexpectedly".format(type(e)))

        # upload only file
        try:
            await self.pet_api.upload_file(pet_id=self.pet.id, file=self.foo)
        except ApiException as e:
            self.fail("upload_file() raised {0} unexpectedly".format(type(e)))

    @async_test
    async def test_delete_pet(self):
        await self.pet_api.add_pet(self.pet)
        await self.pet_api.delete_pet(pet_id=self.pet.id, api_key="special-key")

        try:
            await self.pet_api.get_pet_by_id(pet_id=self.pet.id)
            raise Exception("expected an error")
        except ApiException as e:
            self.assertEqual(404, e.status)

    @async_test
    async def test_proxy(self):
        config = Configuration()
        # set not-existent proxy and catch an error to verify that
        # the client library (aiohttp) tried to use it.
        config.proxy = 'http://localhost:8080/proxy'
        async with petstore_api.ApiClient(config) as client:
            pet_api = petstore_api.PetApi(client)

            with self.assertRaisesRegex(petstore_api.rest.aiohttp.client_exceptions.ClientProxyConnectionError,
                                        'Cannot connect to host localhost:8080'):
                await pet_api.get_pet_by_id(self.pet.id)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
