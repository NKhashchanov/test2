<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <h1>SQL Trainer</h1>
        </div>
        <div class="nav-links">
          <router-link to="/exercises" class="nav-link" @click="handleExercisesClick">Задания</router-link>
          <template v-if="!isAuthenticated">
            <router-link to="/login" class="nav-link">Вход</router-link>
            <router-link to="/register" class="nav-link">Регистрация</router-link>
          </template>
          <template v-else>
            <router-link to="/profile" class="nav-link">Личный кабинет</router-link>
            <button @click="logout" class="nav-link logout-btn">Выйти</button>
          </template>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view ref="routerView"></router-view>
    </main>
  </div>
</template>

<script>
import { useUserStore } from './stores/user'
import { computed, ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    const routerView = ref(null)

    const isAuthenticated = computed(() => userStore.isAuthenticated)

    const logout = () => {
      userStore.logout()
      router.push('/login')
    }

    // Обработчик клика по кнопке "Задания"
    const handleExercisesClick = async () => {
      // Ждем обновления DOM после навигации
      await nextTick()
      
      // Получаем ссылку на компонент Exercises через router-view
      if (routerView.value && routerView.value.$.setupState) {
        const exercisesComponent = routerView.value.$.setupState
        
        // Если компонент Exercises имеет метод forceCloseEditor, вызываем его
        if (exercisesComponent.forceCloseEditor) {
          exercisesComponent.forceCloseEditor()
        }
      }
    }

    return {
      isAuthenticated,
      logout,
      handleExercisesClick,
      routerView
    }
  }
}
</script>