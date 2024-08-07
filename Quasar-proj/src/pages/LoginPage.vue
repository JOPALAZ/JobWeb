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

<script>
import { Notify } from 'quasar';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login(event) {
      event.preventDefault();
      try {
        const response = await this.$axios.post('/api/api-token-auth/', {
          username: this.username,
          password: this.password
        });
        localStorage.setItem('token', response.data.token);
        window.location.replace('/');
      } catch (error) {
        let errorMessage = 'Login failed, try again.';
        if (error.response) {
          errorMessage = error.response.data.non_field_errors
            ? error.response.data.non_field_errors.join(' ')
            : errorMessage;
        }
        Notify.create({
          message: errorMessage,
          color: 'negative',
          position: 'top'
        });
      }
    },
    cancel() {
      this.username = '';
      this.password = '';
    }
  }
};
</script>

<style scoped>
</style>
