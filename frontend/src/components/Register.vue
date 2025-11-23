<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Регистрация</h2>
      <form @submit.prevent="register" class="auth-form">
        <div class="form-group">
          <label>Email:</label>
          <input 
            type="email" 
            v-model="form.email" 
            required 
            placeholder="Введите email"
          >
        </div>
        
        <div class="form-group">
          <label>Имя пользователя:</label>
          <input 
            type="text" 
            v-model="form.username" 
            required 
            placeholder="Введите имя пользователя"
          >
        </div>

        <div class="form-group">
          <label>Пароль:</label>
          <input 
            type="password" 
            v-model="form.password" 
            required 
            placeholder="Введите пароль"
          >
        </div>

        <button type="submit" :disabled="loading" class="auth-btn">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="auth-switch">
        Уже есть аккаунт? <router-link to="/login">Войдите</router-link>
      </p>

      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default {
  name: 'Register',
  setup() {
    const form = ref({
      email: '',
      username: '',
      password: ''
    })
    const loading = ref(false)
    const message = ref('')
    const messageType = ref('')
    const router = useRouter()
    const userStore = useUserStore()

    const register = async () => {
      loading.value = true
      message.value = ''

      try {
        const response = await axios.post(`${API_URL}/users/`, form.value)
        userStore.setUser(response.data)
        message.value = 'Регистрация успешна!'
        messageType.value = 'success'
        setTimeout(() => {
          router.push('/exercises')
        }, 1000)
      } catch (error) {
        if (error.response && error.response.data.detail) {
          message.value = `Ошибка: ${error.response.data.detail}`
        } else {
          message.value = 'Ошибка при регистрации'
        }
        messageType.value = 'error'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      message,
      messageType,
      register
    }
  }
}
</script>