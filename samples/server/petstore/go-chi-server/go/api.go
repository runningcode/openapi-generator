/*
 * OpenAPI Petstore
 *
 * This is a sample server Petstore server. For this sample, you can use the api key `special-key` to test the authorization filters.
 *
 * API version: 1.0.0
 * Generated by: OpenAPI Generator (https://openapi-generator.tech)
 */

package petstoreserver

import (
	"context"
	"net/http"
	"time"
	"os"
)



// PetAPIRouter defines the required methods for binding the api requests to a responses for the PetAPI
// The PetAPIRouter implementation should parse necessary information from the http request,
// pass the data to a PetAPIServicer to perform the required actions, then write the service results to the http response.
type PetAPIRouter interface { 
	AddPet(http.ResponseWriter, *http.Request)
	DeletePet(http.ResponseWriter, *http.Request)
	FilterPetsByCategory(http.ResponseWriter, *http.Request)
	FindPetsByStatus(http.ResponseWriter, *http.Request)
	// Deprecated
	FindPetsByTags(http.ResponseWriter, *http.Request)
	GetPetById(http.ResponseWriter, *http.Request)
	GetPetImageById(http.ResponseWriter, *http.Request)
	GetPetsUsingBooleanQueryParameters(http.ResponseWriter, *http.Request)
	UpdatePet(http.ResponseWriter, *http.Request)
	UpdatePetWithForm(http.ResponseWriter, *http.Request)
	UploadFile(http.ResponseWriter, *http.Request)
	UploadFileArrayOfFiles(http.ResponseWriter, *http.Request)
}
// StoreAPIRouter defines the required methods for binding the api requests to a responses for the StoreAPI
// The StoreAPIRouter implementation should parse necessary information from the http request,
// pass the data to a StoreAPIServicer to perform the required actions, then write the service results to the http response.
type StoreAPIRouter interface { 
	DeleteOrder(http.ResponseWriter, *http.Request)
	GetInventory(http.ResponseWriter, *http.Request)
	GetOrderById(http.ResponseWriter, *http.Request)
	PlaceOrder(http.ResponseWriter, *http.Request)
}
// UserAPIRouter defines the required methods for binding the api requests to a responses for the UserAPI
// The UserAPIRouter implementation should parse necessary information from the http request,
// pass the data to a UserAPIServicer to perform the required actions, then write the service results to the http response.
type UserAPIRouter interface { 
	CreateUser(http.ResponseWriter, *http.Request)
	CreateUsersWithArrayInput(http.ResponseWriter, *http.Request)
	CreateUsersWithListInput(http.ResponseWriter, *http.Request)
	DeleteUser(http.ResponseWriter, *http.Request)
	GetUserByName(http.ResponseWriter, *http.Request)
	LoginUser(http.ResponseWriter, *http.Request)
	LogoutUser(http.ResponseWriter, *http.Request)
	UpdateUser(http.ResponseWriter, *http.Request)
}


// PetAPIServicer defines the api actions for the PetAPI service
// This interface intended to stay up to date with the openapi yaml used to generate it,
// while the service implementation can be ignored with the .openapi-generator-ignore file
// and updated with the logic required for the API.
type PetAPIServicer interface { 
	AddPet(context.Context, Pet) (ImplResponse, error)
	DeletePet(context.Context, int64, string) (ImplResponse, error)
	FilterPetsByCategory(context.Context, Gender, Species, []Species) (ImplResponse, error)
	FindPetsByStatus(context.Context, []string) (ImplResponse, error)
	// Deprecated
	FindPetsByTags(context.Context, []string, time.Time, time.Time) (ImplResponse, error)
	GetPetById(context.Context, int64) (ImplResponse, error)
	GetPetImageById(context.Context, int64) (ImplResponse, error)
	GetPetsUsingBooleanQueryParameters(context.Context, bool, bool, bool) (ImplResponse, error)
	UpdatePet(context.Context, Pet) (ImplResponse, error)
	UpdatePetWithForm(context.Context, int64, string, string) (ImplResponse, error)
	UploadFile(context.Context, int64, string, *os.File) (ImplResponse, error)
	UploadFileArrayOfFiles(context.Context, int64, string, []*os.File) (ImplResponse, error)
}


// StoreAPIServicer defines the api actions for the StoreAPI service
// This interface intended to stay up to date with the openapi yaml used to generate it,
// while the service implementation can be ignored with the .openapi-generator-ignore file
// and updated with the logic required for the API.
type StoreAPIServicer interface { 
	DeleteOrder(context.Context, string) (ImplResponse, error)
	GetInventory(context.Context) (ImplResponse, error)
	GetOrderById(context.Context, int64) (ImplResponse, error)
	PlaceOrder(context.Context, Order) (ImplResponse, error)
}


// UserAPIServicer defines the api actions for the UserAPI service
// This interface intended to stay up to date with the openapi yaml used to generate it,
// while the service implementation can be ignored with the .openapi-generator-ignore file
// and updated with the logic required for the API.
type UserAPIServicer interface { 
	CreateUser(context.Context, User) (ImplResponse, error)
	CreateUsersWithArrayInput(context.Context, []User) (ImplResponse, error)
	CreateUsersWithListInput(context.Context, []User) (ImplResponse, error)
	DeleteUser(context.Context, string, bool) (ImplResponse, error)
	GetUserByName(context.Context, string) (ImplResponse, error)
	LoginUser(context.Context, string, string, bool) (ImplResponse, error)
	LogoutUser(context.Context) (ImplResponse, error)
	UpdateUser(context.Context, string, User) (ImplResponse, error)
}
