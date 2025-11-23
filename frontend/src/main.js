import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './styles/style.css'

// Компоненты страниц
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import Exercises from './components/Exercises.vue'
import Profile from './components/Profile.vue'

const routes = [
  { path: '/', redirect: '/exercises' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/exercises', component: Exercises },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Навигационный guard для защиты маршрутов
router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'))
  if (to.meta.requiresAuth && !user) {
    next('/login')
  } else {
    next()
  }
})

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// Инициализируем состояние пользователя
import { useUserStore } from './stores/user'
const userStore = useUserStore()
userStore.initialize()

app.mount('#app')

// Глобальная переменная для хранения ссылки на компонент Exercises
let exercisesComponent = null

// Глобальный метод для установки ссылки на компонент
app.config.globalProperties.$setExercisesComponent = (component) => {
  exercisesComponent = component
}

// Глобальный метод для получения ссылки на компонент
app.config.globalProperties.$getExercisesComponent = () => {
  return exercisesComponent
}