import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  
  const isAuthenticated = computed(() => !!user.value)
  
  const setUser = (userData) => {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }
  
  const logout = () => {
    user.value = null
    localStorage.removeItem('user')
  }
  
  const initialize = () => {
    const userData = localStorage.getItem('user')
    if (userData) {
      user.value = JSON.parse(userData)
    }
  }
  
  return {
    user,
    isAuthenticated,
    setUser,
    logout,
    initialize
  }
})