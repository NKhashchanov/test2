<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Вход в систему</h2>
      <form @submit.prevent="login" class="auth-form">
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
          <label>Пароль:</label>
          <input 
            type="password" 
            v-model="form.password" 
            required 
            placeholder="Введите пароль"
          >
        </div>

        <button type="submit" :disabled="loading" class="auth-btn">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>

      <p class="auth-switch">
        Нет аккаунта? <router-link to="/register">Зарегистрируйтесь</router-link>
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
  name: 'Login',
  setup() {
    const form = ref({
      email: '',
      password: ''
    })
    const loading = ref(false)
    const message = ref('')
    const messageType = ref('')
    const router = useRouter()
    const userStore = useUserStore()

    const login = async () => {
      loading.value = true
      message.value = ''

      try {
        // Ищем пользователя по email
        const response = await axios.get(`${API_URL}/users/`)
        const users = response.data
        const user = users.find(u => u.email === form.value.email)
        
        if (user) {
          userStore.setUser(user)
          message.value = 'Успешный вход!'
          messageType.value = 'success'
          setTimeout(() => {
            router.push('/exercises')
          }, 1000)
        } else {
          message.value = 'Пользователь не найден'
          messageType.value = 'error'
        }
      } catch (error) {
        message.value = 'Ошибка при входе'
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
      login
    }
  }
}
</script>