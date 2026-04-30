# Generated TypeScript README
This README will guide you through the process of using the generated JavaScript SDK package for the connector `example`. It will also provide examples on how to use your generated SDK to call your Data Connect queries and mutations.

***NOTE:** This README is generated alongside the generated SDK. If you make changes to this file, they will be overwritten when the SDK is regenerated.*

# Table of Contents
- [**Overview**](#generated-javascript-readme)
- [**Accessing the connector**](#accessing-the-connector)
  - [*Connecting to the local Emulator*](#connecting-to-the-local-emulator)
- [**Queries**](#queries)
  - [*AllMovies*](#allmovies)
  - [*MyMovieLists*](#mymovielists)
- [**Mutations**](#mutations)
  - [*CreateMovieList*](#createmovielist)
  - [*AddMovieToMovieList*](#addmovietomovielist)

# Accessing the connector
A connector is a collection of Queries and Mutations. One SDK is generated for each connector - this SDK is generated for the connector `example`. You can find more information about connectors in the [Data Connect documentation](https://firebase.google.com/docs/data-connect#how-does).

You can use this generated SDK by importing from the package `@dataconnect/generated` as shown below. Both CommonJS and ESM imports are supported.

You can also follow the instructions from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#set-client).

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig } from '@dataconnect/generated';

const dataConnect = getDataConnect(connectorConfig);
```

## Connecting to the local Emulator
By default, the connector will connect to the production service.

To connect to the emulator, you can use the following code.
You can also follow the emulator instructions from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#instrument-clients).

```typescript
import { connectDataConnectEmulator, getDataConnect } from 'firebase/data-connect';
import { connectorConfig } from '@dataconnect/generated';

const dataConnect = getDataConnect(connectorConfig);
connectDataConnectEmulator(dataConnect, 'localhost', 9399);
```

After it's initialized, you can call your Data Connect [queries](#queries) and [mutations](#mutations) from your generated SDK.

# Queries

There are two ways to execute a Data Connect Query using the generated Web SDK:
- Using a Query Reference function, which returns a `QueryRef`
  - The `QueryRef` can be used as an argument to `executeQuery()`, which will execute the Query and return a `QueryPromise`
- Using an action shortcut function, which returns a `QueryPromise`
  - Calling the action shortcut function will execute the Query and return a `QueryPromise`

The following is true for both the action shortcut function and the `QueryRef` function:
- The `QueryPromise` returned will resolve to the result of the Query once it has finished executing
- If the Query accepts arguments, both the action shortcut function and the `QueryRef` function accept a single argument: an object that contains all the required variables (and the optional variables) for the Query
- Both functions can be called with or without passing in a `DataConnect` instance as an argument. If no `DataConnect` argument is passed in, then the generated SDK will call `getDataConnect(connectorConfig)` behind the scenes for you.

Below are examples of how to use the `example` connector's generated functions to execute each query. You can also follow the examples from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#using-queries).

## AllMovies
You can execute the `AllMovies` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
allMovies(options?: ExecuteQueryOptions): QueryPromise<AllMoviesData, undefined>;

interface AllMoviesRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<AllMoviesData, undefined>;
}
export const allMoviesRef: AllMoviesRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
allMovies(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<AllMoviesData, undefined>;

interface AllMoviesRef {
  ...
  (dc: DataConnect): QueryRef<AllMoviesData, undefined>;
}
export const allMoviesRef: AllMoviesRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the allMoviesRef:
```typescript
const name = allMoviesRef.operationName;
console.log(name);
```

### Variables
The `AllMovies` query has no variables.
### Return Type
Recall that executing the `AllMovies` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `AllMoviesData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface AllMoviesData {
  movies: ({
    id: UUIDString;
    title: string;
    year: number;
    genres?: string[] | null;
    summary?: string | null;
    posterUrl?: string | null;
    createdAt: TimestampString;
  } & Movie_Key)[];
}
```
### Using `AllMovies`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, allMovies } from '@dataconnect/generated';


// Call the `allMovies()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await allMovies();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await allMovies(dataConnect);

console.log(data.movies);

// Or, you can use the `Promise` API.
allMovies().then((response) => {
  const data = response.data;
  console.log(data.movies);
});
```

### Using `AllMovies`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, allMoviesRef } from '@dataconnect/generated';


// Call the `allMoviesRef()` function to get a reference to the query.
const ref = allMoviesRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = allMoviesRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.movies);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.movies);
});
```

## MyMovieLists
You can execute the `MyMovieLists` query using the following action shortcut function, or by calling `executeQuery()` after calling the following `QueryRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
myMovieLists(options?: ExecuteQueryOptions): QueryPromise<MyMovieListsData, undefined>;

interface MyMovieListsRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<MyMovieListsData, undefined>;
}
export const myMovieListsRef: MyMovieListsRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `QueryRef` function.
```typescript
myMovieLists(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<MyMovieListsData, undefined>;

interface MyMovieListsRef {
  ...
  (dc: DataConnect): QueryRef<MyMovieListsData, undefined>;
}
export const myMovieListsRef: MyMovieListsRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the myMovieListsRef:
```typescript
const name = myMovieListsRef.operationName;
console.log(name);
```

### Variables
The `MyMovieLists` query has no variables.
### Return Type
Recall that executing the `MyMovieLists` query returns a `QueryPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `MyMovieListsData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface MyMovieListsData {
  movieLists: ({
    id: UUIDString;
    name: string;
    public: boolean;
    description?: string | null;
    shareableLink?: string | null;
    createdAt: TimestampString;
    updatedAt: TimestampString;
    movieListEntries_on_movieList: ({
      id: UUIDString;
      position: number;
      note?: string | null;
      movie: {
        id: UUIDString;
        title: string;
        year: number;
      } & Movie_Key;
    } & MovieListEntry_Key)[];
  } & MovieList_Key)[];
}
```
### Using `MyMovieLists`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, myMovieLists } from '@dataconnect/generated';


// Call the `myMovieLists()` function to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await myMovieLists();

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await myMovieLists(dataConnect);

console.log(data.movieLists);

// Or, you can use the `Promise` API.
myMovieLists().then((response) => {
  const data = response.data;
  console.log(data.movieLists);
});
```

### Using `MyMovieLists`'s `QueryRef` function

```typescript
import { getDataConnect, executeQuery } from 'firebase/data-connect';
import { connectorConfig, myMovieListsRef } from '@dataconnect/generated';


// Call the `myMovieListsRef()` function to get a reference to the query.
const ref = myMovieListsRef();

// You can also pass in a `DataConnect` instance to the `QueryRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = myMovieListsRef(dataConnect);

// Call `executeQuery()` on the reference to execute the query.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeQuery(ref);

console.log(data.movieLists);

// Or, you can use the `Promise` API.
executeQuery(ref).then((response) => {
  const data = response.data;
  console.log(data.movieLists);
});
```

# Mutations

There are two ways to execute a Data Connect Mutation using the generated Web SDK:
- Using a Mutation Reference function, which returns a `MutationRef`
  - The `MutationRef` can be used as an argument to `executeMutation()`, which will execute the Mutation and return a `MutationPromise`
- Using an action shortcut function, which returns a `MutationPromise`
  - Calling the action shortcut function will execute the Mutation and return a `MutationPromise`

The following is true for both the action shortcut function and the `MutationRef` function:
- The `MutationPromise` returned will resolve to the result of the Mutation once it has finished executing
- If the Mutation accepts arguments, both the action shortcut function and the `MutationRef` function accept a single argument: an object that contains all the required variables (and the optional variables) for the Mutation
- Both functions can be called with or without passing in a `DataConnect` instance as an argument. If no `DataConnect` argument is passed in, then the generated SDK will call `getDataConnect(connectorConfig)` behind the scenes for you.

Below are examples of how to use the `example` connector's generated functions to execute each mutation. You can also follow the examples from the [Data Connect documentation](https://firebase.google.com/docs/data-connect/web-sdk#using-mutations).

## CreateMovieList
You can execute the `CreateMovieList` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
createMovieList(vars: CreateMovieListVariables): MutationPromise<CreateMovieListData, CreateMovieListVariables>;

interface CreateMovieListRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateMovieListVariables): MutationRef<CreateMovieListData, CreateMovieListVariables>;
}
export const createMovieListRef: CreateMovieListRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
createMovieList(dc: DataConnect, vars: CreateMovieListVariables): MutationPromise<CreateMovieListData, CreateMovieListVariables>;

interface CreateMovieListRef {
  ...
  (dc: DataConnect, vars: CreateMovieListVariables): MutationRef<CreateMovieListData, CreateMovieListVariables>;
}
export const createMovieListRef: CreateMovieListRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the createMovieListRef:
```typescript
const name = createMovieListRef.operationName;
console.log(name);
```

### Variables
The `CreateMovieList` mutation requires an argument of type `CreateMovieListVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface CreateMovieListVariables {
  name: string;
  public: boolean;
  description?: string | null;
}
```
### Return Type
Recall that executing the `CreateMovieList` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `CreateMovieListData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface CreateMovieListData {
  movieList_insert: MovieList_Key;
}
```
### Using `CreateMovieList`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, createMovieList, CreateMovieListVariables } from '@dataconnect/generated';

// The `CreateMovieList` mutation requires an argument of type `CreateMovieListVariables`:
const createMovieListVars: CreateMovieListVariables = {
  name: ..., 
  public: ..., 
  description: ..., // optional
};

// Call the `createMovieList()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await createMovieList(createMovieListVars);
// Variables can be defined inline as well.
const { data } = await createMovieList({ name: ..., public: ..., description: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await createMovieList(dataConnect, createMovieListVars);

console.log(data.movieList_insert);

// Or, you can use the `Promise` API.
createMovieList(createMovieListVars).then((response) => {
  const data = response.data;
  console.log(data.movieList_insert);
});
```

### Using `CreateMovieList`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, createMovieListRef, CreateMovieListVariables } from '@dataconnect/generated';

// The `CreateMovieList` mutation requires an argument of type `CreateMovieListVariables`:
const createMovieListVars: CreateMovieListVariables = {
  name: ..., 
  public: ..., 
  description: ..., // optional
};

// Call the `createMovieListRef()` function to get a reference to the mutation.
const ref = createMovieListRef(createMovieListVars);
// Variables can be defined inline as well.
const ref = createMovieListRef({ name: ..., public: ..., description: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = createMovieListRef(dataConnect, createMovieListVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.movieList_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.movieList_insert);
});
```

## AddMovieToMovieList
You can execute the `AddMovieToMovieList` mutation using the following action shortcut function, or by calling `executeMutation()` after calling the following `MutationRef` function, both of which are defined in [dataconnect-generated/index.d.ts](./index.d.ts):
```typescript
addMovieToMovieList(vars: AddMovieToMovieListVariables): MutationPromise<AddMovieToMovieListData, AddMovieToMovieListVariables>;

interface AddMovieToMovieListRef {
  ...
  /* Allow users to create refs without passing in DataConnect */
  (vars: AddMovieToMovieListVariables): MutationRef<AddMovieToMovieListData, AddMovieToMovieListVariables>;
}
export const addMovieToMovieListRef: AddMovieToMovieListRef;
```
You can also pass in a `DataConnect` instance to the action shortcut function or `MutationRef` function.
```typescript
addMovieToMovieList(dc: DataConnect, vars: AddMovieToMovieListVariables): MutationPromise<AddMovieToMovieListData, AddMovieToMovieListVariables>;

interface AddMovieToMovieListRef {
  ...
  (dc: DataConnect, vars: AddMovieToMovieListVariables): MutationRef<AddMovieToMovieListData, AddMovieToMovieListVariables>;
}
export const addMovieToMovieListRef: AddMovieToMovieListRef;
```

If you need the name of the operation without creating a ref, you can retrieve the operation name by calling the `operationName` property on the addMovieToMovieListRef:
```typescript
const name = addMovieToMovieListRef.operationName;
console.log(name);
```

### Variables
The `AddMovieToMovieList` mutation requires an argument of type `AddMovieToMovieListVariables`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:

```typescript
export interface AddMovieToMovieListVariables {
  movieListId: UUIDString;
  movieId: UUIDString;
  position: number;
  note?: string | null;
}
```
### Return Type
Recall that executing the `AddMovieToMovieList` mutation returns a `MutationPromise` that resolves to an object with a `data` property.

The `data` property is an object of type `AddMovieToMovieListData`, which is defined in [dataconnect-generated/index.d.ts](./index.d.ts). It has the following fields:
```typescript
export interface AddMovieToMovieListData {
  movieListEntry_insert: MovieListEntry_Key;
}
```
### Using `AddMovieToMovieList`'s action shortcut function

```typescript
import { getDataConnect } from 'firebase/data-connect';
import { connectorConfig, addMovieToMovieList, AddMovieToMovieListVariables } from '@dataconnect/generated';

// The `AddMovieToMovieList` mutation requires an argument of type `AddMovieToMovieListVariables`:
const addMovieToMovieListVars: AddMovieToMovieListVariables = {
  movieListId: ..., 
  movieId: ..., 
  position: ..., 
  note: ..., // optional
};

// Call the `addMovieToMovieList()` function to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await addMovieToMovieList(addMovieToMovieListVars);
// Variables can be defined inline as well.
const { data } = await addMovieToMovieList({ movieListId: ..., movieId: ..., position: ..., note: ..., });

// You can also pass in a `DataConnect` instance to the action shortcut function.
const dataConnect = getDataConnect(connectorConfig);
const { data } = await addMovieToMovieList(dataConnect, addMovieToMovieListVars);

console.log(data.movieListEntry_insert);

// Or, you can use the `Promise` API.
addMovieToMovieList(addMovieToMovieListVars).then((response) => {
  const data = response.data;
  console.log(data.movieListEntry_insert);
});
```

### Using `AddMovieToMovieList`'s `MutationRef` function

```typescript
import { getDataConnect, executeMutation } from 'firebase/data-connect';
import { connectorConfig, addMovieToMovieListRef, AddMovieToMovieListVariables } from '@dataconnect/generated';

// The `AddMovieToMovieList` mutation requires an argument of type `AddMovieToMovieListVariables`:
const addMovieToMovieListVars: AddMovieToMovieListVariables = {
  movieListId: ..., 
  movieId: ..., 
  position: ..., 
  note: ..., // optional
};

// Call the `addMovieToMovieListRef()` function to get a reference to the mutation.
const ref = addMovieToMovieListRef(addMovieToMovieListVars);
// Variables can be defined inline as well.
const ref = addMovieToMovieListRef({ movieListId: ..., movieId: ..., position: ..., note: ..., });

// You can also pass in a `DataConnect` instance to the `MutationRef` function.
const dataConnect = getDataConnect(connectorConfig);
const ref = addMovieToMovieListRef(dataConnect, addMovieToMovieListVars);

// Call `executeMutation()` on the reference to execute the mutation.
// You can use the `await` keyword to wait for the promise to resolve.
const { data } = await executeMutation(ref);

console.log(data.movieListEntry_insert);

// Or, you can use the `Promise` API.
executeMutation(ref).then((response) => {
  const data = response.data;
  console.log(data.movieListEntry_insert);
});
```

