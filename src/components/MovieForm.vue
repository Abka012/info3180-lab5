<template>
  <div class="container mt-4">
    <h2>Add New Movie</h2>

    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
      {{ successMessage }}
      <button type="button" class="btn-close" @click="successMessage = ''"></button>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
      <ul class="mb-0">
        <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
      </ul>
      <button type="button" class="btn-close" @click="errorMessage = ''"></button>
    </div>

    <form id="movieForm" @submit.prevent="saveMovie">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input
          type="text"
          name="title"
          id="title"
          class="form-control"
          v-model="form.title"
          :class="{ 'is-invalid': errors.title }"
        />
        <div v-if="errors.title" class="invalid-feedback">
          {{ errors.title[0] }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          name="description"
          id="description"
          class="form-control"
          rows="5"
          v-model="form.description"
          :class="{ 'is-invalid': errors.description }"
        ></textarea>
        <div v-if="errors.description" class="invalid-feedback">
          {{ errors.description[0] }}
        </div>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input
          type="file"
          name="poster"
          id="poster"
          class="form-control"
          :class="{ 'is-invalid': errors.poster }"
          accept="image/png, image/jpeg, image/gif"
        />
        <div v-if="errors.poster" class="invalid-feedback">
          {{ errors.poster[0] }}
        </div>
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
let successMessage = ref("");
let errorMessage = ref("");
let errors = ref({});

let form = ref({
  title: "",
  description: "",
  poster: null,
});

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    });
}

function saveMovie() {
  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.errors) {
        // Validation failed
        errorMessage.value = "Please correct the errors below.";
        errors.value = data.errors;
        successMessage.value = "";
      } else {
        // Success
        successMessage.value = `${data.message}: ${data.title}`;
        errorMessage.value = "";
        errors.value = {};
        form.value = {
          title: "",
          description: "",
          poster: null,
        };
        // Reset the form
        document.getElementById("movieForm").reset();
      }
    })
    .catch(function (error) {
      console.log(error);
      errorMessage.value = "An error occurred while submitting the form.";
    });
}

onMounted(() => {
  getCsrfToken();
});
</script>

<style scoped>
/* Add any component specific styles here */
</style>
