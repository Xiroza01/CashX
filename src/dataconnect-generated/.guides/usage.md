# Basic Usage

Always prioritize using a supported framework over using the generated SDK
directly. Supported frameworks simplify the developer experience and help ensure
best practices are followed.





## Advanced Usage
If a user is not using a supported framework, they can use the generated SDK directly.

Here's an example of how to use it with the first 5 operations:

```js
import { allMovies, myMovieLists, createMovieList, addMovieToMovieList } from '@dataconnect/generated';


// Operation AllMovies: 
const { data } = await AllMovies(dataConnect);

// Operation MyMovieLists: 
const { data } = await MyMovieLists(dataConnect);

// Operation CreateMovieList:  For variables, look at type CreateMovieListVars in ../index.d.ts
const { data } = await CreateMovieList(dataConnect, createMovieListVars);

// Operation AddMovieToMovieList:  For variables, look at type AddMovieToMovieListVars in ../index.d.ts
const { data } = await AddMovieToMovieList(dataConnect, addMovieToMovieListVars);


```