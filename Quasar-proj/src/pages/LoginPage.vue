<template>
  <q-page class="row justify-center items-center">
    <q-card class="q-pa-md" style="width: 400px">
      <q-card-section>
        <div class="text-h6">Login</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="login">
          <q-input v-model="username" label="Username" required />
          <q-input v-model="password" label="Password" type="password" required />
          <q-btn label="Login" type="submit" color="primary" class="q-mt-md" />
        </q-form>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Cancel" color="primary" @click="cancel" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { Notify } from 'quasar';

const username = ref('');
const password = ref('');

const login = async (event) => {
  event.preventDefault();
  try {
    const response = await axios.post('http://localhost:8000/api/api-token-auth/', {
      username: username.value,
      password: password.value,
    });
    localStorage.setItem('token', response.data['token']);
    window.location.replace('/')
  } catch (error) {
    Notify.create({
          message: 'Login failed, try again.',
          color: 'negative',
          position: 'top'
        });
  }
};

const cancel = () => {
  username.value = '';
  password.value = '';
};
</script>

<style scoped>
</style>
