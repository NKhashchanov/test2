<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>Личный кабинет</h2>
      <div v-if="user" class="user-info">
        <div class="info-item">
          <label>ID пользователя:</label>
          <span>{{ user.user_id }}</span>
        </div>
        <div class="info-item">
          <label>Имя пользователя:</label>
          <span>{{ user.username }}</span>
        </div>
        <div class="info-item">
          <label>Email:</label>
          <span>{{ user.email }}</span>
        </div>
        <div class="info-item">
          <label>Дата регистрации:</label>
          <span>{{ formatDate(user.created_at) }}</span>
        </div>
        <div class="stats-section">
          <h3>Статистика</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-value">{{ completedExercises }}</div>
              <div class="stat-label">Выполнено заданий</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ totalExercises }}</div>
              <div class="stat-label">Всего заданий</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ completionRate }}%</div>
              <div class="stat-label">Процент выполнения</div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="not-authorized">
        <p>Для просмотра личного кабинета необходимо авторизоваться</p>
        <router-link to="/login" class="auth-link">Войти</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '../stores/user'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default {
  name: 'Profile',
  setup() {
    const userStore = useUserStore()
    const user = ref(userStore.user)
    const userExercises = ref([])
    const exercises = ref([])

    const fetchUserExercises = async () => {
      if (!user.value) return
      
      try {
        const response = await axios.get(`${API_URL}/user-exercises/user/${user.value.user_id}`)
        userExercises.value = response.data
      } catch (error) {
        console.error('Error fetching user exercises:', error)
      }
    }

    const fetchExercises = async () => {
      try {
        const response = await axios.get(`${API_URL}/exercises/`)
        exercises.value = response.data
      } catch (error) {
        console.error('Error fetching exercises:', error)
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const completedExercises = computed(() => {
      return userExercises.value.filter(ue => ue.completed).length
    })

    const totalExercises = computed(() => {
      return exercises.value.length
    })

    const completionRate = computed(() => {
      if (totalExercises.value === 0) return 0
      return Math.round((completedExercises.value / totalExercises.value) * 100)
    })

    onMounted(() => {
      fetchUserExercises()
      fetchExercises()
    })

    return {
      user,
      completedExercises,
      totalExercises,
      completionRate,
      formatDate
    }
  }
}
</script>