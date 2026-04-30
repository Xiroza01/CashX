import { ConnectorConfig, DataConnect, QueryRef, QueryPromise, ExecuteQueryOptions, MutationRef, MutationPromise, DataConnectSettings } from 'firebase/data-connect';

export const connectorConfig: ConnectorConfig;
export const dataConnectSettings: DataConnectSettings;

export type TimestampString = string;
export type UUIDString = string;
export type Int64String = string;
export type DateString = string;




export interface AddMovieToMovieListData {
  movieListEntry_insert: MovieListEntry_Key;
}

export interface AddMovieToMovieListVariables {
  movieListId: UUIDString;
  movieId: UUIDString;
  position: number;
  note?: string | null;
}

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

export interface CreateMovieListData {
  movieList_insert: MovieList_Key;
}

export interface CreateMovieListVariables {
  name: string;
  public: boolean;
  description?: string | null;
}

export interface MovieListEntry_Key {
  id: UUIDString;
  __typename?: 'MovieListEntry_Key';
}

export interface MovieList_Key {
  id: UUIDString;
  __typename?: 'MovieList_Key';
}

export interface Movie_Key {
  id: UUIDString;
  __typename?: 'Movie_Key';
}

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

export interface Review_Key {
  id: UUIDString;
  __typename?: 'Review_Key';
}

export interface User_Key {
  id: UUIDString;
  __typename?: 'User_Key';
}

export interface Watch_Key {
  id: UUIDString;
  __typename?: 'Watch_Key';
}

interface AllMoviesRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<AllMoviesData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<AllMoviesData, undefined>;
  operationName: string;
}
export const allMoviesRef: AllMoviesRef;

export function allMovies(options?: ExecuteQueryOptions): QueryPromise<AllMoviesData, undefined>;
export function allMovies(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<AllMoviesData, undefined>;

interface MyMovieListsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<MyMovieListsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<MyMovieListsData, undefined>;
  operationName: string;
}
export const myMovieListsRef: MyMovieListsRef;

export function myMovieLists(options?: ExecuteQueryOptions): QueryPromise<MyMovieListsData, undefined>;
export function myMovieLists(dc: DataConnect, options?: ExecuteQueryOptions): QueryPromise<MyMovieListsData, undefined>;

interface CreateMovieListRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateMovieListVariables): MutationRef<CreateMovieListData, CreateMovieListVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateMovieListVariables): MutationRef<CreateMovieListData, CreateMovieListVariables>;
  operationName: string;
}
export const createMovieListRef: CreateMovieListRef;

export function createMovieList(vars: CreateMovieListVariables): MutationPromise<CreateMovieListData, CreateMovieListVariables>;
export function createMovieList(dc: DataConnect, vars: CreateMovieListVariables): MutationPromise<CreateMovieListData, CreateMovieListVariables>;

interface AddMovieToMovieListRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: AddMovieToMovieListVariables): MutationRef<AddMovieToMovieListData, AddMovieToMovieListVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: AddMovieToMovieListVariables): MutationRef<AddMovieToMovieListData, AddMovieToMovieListVariables>;
  operationName: string;
}
export const addMovieToMovieListRef: AddMovieToMovieListRef;

export function addMovieToMovieList(vars: AddMovieToMovieListVariables): MutationPromise<AddMovieToMovieListData, AddMovieToMovieListVariables>;
export function addMovieToMovieList(dc: DataConnect, vars: AddMovieToMovieListVariables): MutationPromise<AddMovieToMovieListData, AddMovieToMovieListVariables>;

