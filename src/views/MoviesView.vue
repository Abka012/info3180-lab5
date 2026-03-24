<template>
  <div class="container mt-4">
    <h2>All Movies</h2>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="movies.length === 0" class="alert alert-info">
      No movies found. <RouterLink to="/movies/create" class="alert-link">Add your first movie</RouterLink>.
    </div>

    <div v-else class="row">
      <div v-for="movie in movies" :key="movie.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <img v-if="movie.poster" :src="movie.poster" class="card-img-top" :alt="movie.title" style="height: 200px; object-fit: cover;" />
          <img v-else class="card-img-top" src="/placeholder-movie.png" alt="No poster available" style="height: 200px; object-fit: cover;" />
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text">{{ movie.description }}</p>
          </div>
          <div class="card-footer">
            <small class="text-muted">ID: {{ movie.id }}</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);
let loading = ref(true);

function fetchMovies() {
  fetch("/api/v1/movies")
    .then((response) => response.json())
    .then((data) => {
      movies.value = data.movies;
      loading.value = false;
    })
    .catch((error) => {
      console.log(error);
      loading.value = false;
    });
}

onMounted(() => {
  fetchMovies();
});
</script>

<style scoped>
/* Add any component specific styles here */
</style>
