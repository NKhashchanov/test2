<template>
  <div class="exercises-container">
    <!-- Режим списка заданий -->
    <div v-if="!selectedExercise" class="exercises-list-mode">
      <div class="filters-section">
        <h2>SQL Задания</h2>
        
        <div class="filters">
          <div class="filter-group">
            <label>Сложность:</label>
            <select v-model="filters.difficulty" @change="applyFilters">
              <option value="">Все</option>
              <option v-for="diff in difficulties" :key="diff.task_difficulty_id" :value="diff.task_difficulty_id">
                {{ diff.task_difficulty_name }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Тема:</label>
            <select v-model="filters.theme" @change="applyFilters">
              <option value="">Все</option>
              <option v-for="theme in themes" :key="theme.task_theme_id" :value="theme.task_theme_id">
                {{ theme.task_theme_name }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Заданий на странице:</label>
            <select v-model.number="pageSize" @change="updatePagination">
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
        </div>
      </div>

      <div class="exercises-table-container">
        <table class="exercises-table">
          <thead>
            <tr>
              <th @click="sortBy('difficulty')" class="sortable">
                Сложность 
                <span v-if="sortField === 'difficulty'" class="sort-arrow">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('exercises_id')" class="sortable">
                ID
                <span v-if="sortField === 'exercises_id'" class="sort-arrow">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('exercises_name')" class="sortable">
                Название
                <span v-if="sortField === 'exercises_name'" class="sort-arrow">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th @click="sortBy('completed')" class="sortable">
                Статус
                <span v-if="sortField === 'completed'" class="sort-arrow">
                  {{ sortDirection === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="exercise in displayedExercises" :key="exercise.exercises_id" class="exercise-row">
              <td>
                <span class="difficulty-badge" :class="getDifficultyClass(exercise.difficulty)">
                  {{ exercise.difficulty?.task_difficulty_name || 'Нет данных' }}
                </span>
              </td>
              <td>{{ exercise.exercises_id }}</td>
              <td class="exercise-title">{{ exercise.exercises_name }}</td>
              <td>
                <span v-if="isCompleted(exercise.exercises_id)" class="status completed">✓ Выполнено</span>
                <span v-else class="status pending">⏳ Не выполнено</span>
              </td>
              <td>
                <button 
                  @click="openExercise(exercise)" 
                  class="action-btn"
                >
                  Решить
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Пагинация -->
        <div class="pagination" v-if="totalPages > 1">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1"
            class="pagination-btn"
          >
            Назад
          </button>
          
          <span class="pagination-info">
            Страница {{ currentPage }} из {{ totalPages }}
          </span>
          
          <button 
            @click="nextPage" 
            :disabled="currentPage === totalPages"
            class="pagination-btn"
          >
            Вперед
          </button>
        </div>

        <div v-if="loading" class="loading">Загрузка...</div>
        <div v-if="!loading && filteredExercises.length === 0" class="no-data">
          Задания не найдены
        </div>
      </div>
    </div>

    <!-- Режим редактора кода -->
    <div v-else class="editor-mode">
      <!-- Верхняя панель -->
      <div class="editor-header">
        <button @click="closeExercise" class="back-btn">
          ← Назад к списку
        </button>
        <div class="exercise-meta">
          <span class="difficulty-badge" :class="getDifficultyClass(selectedExercise.difficulty)">
            {{ selectedExercise.difficulty?.task_difficulty_name }}
          </span>
          <span class="theme-badge">
            {{ selectedExercise.theme?.task_theme_name }}
          </span>
        </div>
      </div>

      <!-- Основное окно с двумя панелями и разделителем -->
      <div class="editor-main" ref="editorMain">
        <!-- Левая панель - описание -->
        <div 
          class="left-panel" 
          ref="leftPanel"
          :style="{ width: leftPanelWidth + 'px' }"
        >
          <div class="panel-content">
            <h2 class="exercise-title">{{ selectedExercise.exercises_name }}</h2>
            
            <div class="description-section">
              <h3>Описание задания</h3>
              <p>{{ selectedExercise.description }}</p>
            </div>

            <div class="hints-section">
              <h3>Подсказки</h3>
              <ul>
                <li>Внимательно прочитайте условие задания</li>
                <li>Используйте правильный синтаксис SQL</li>
                <li>Проверяйте запрос на ошибки перед отправкой</li>
                <li>Убедитесь, что ваш запрос соответствует требованию</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Разделитель панелей -->
        <div 
          class="panel-divider" 
          @mousedown="startResize"
          @touchstart="startResize"
        ></div>

        <!-- Правая панель - редактор -->
        <div class="right-panel">
          <div class="panel-content">
            <div class="editor-container">
              <label class="editor-label">Ваш SQL запрос:</label>
              <codemirror
                v-model="userQuery"
                :extensions="extensions"
                :autofocus="true"
                :tab-size="2"
                placeholder="Напишите ваш SQL запрос здесь..."
                class="code-editor"
              />
            </div>

            <div class="editor-actions">
              <button @click="clearCode" class="secondary-btn">
                Очистить редактор
              </button>
              <button @click="submitSolution" class="submit-btn">
                Отправить на проверку
              </button>
            </div>

            <div class="result-section" v-if="submissionResult">
              <h3>Результат проверки</h3>
              <div :class="['result-message', submissionResult.type]">
                {{ submissionResult.message }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, nextTick, onUnmounted } from 'vue'
import { useUserStore } from '../stores/user'
import { Codemirror } from 'vue-codemirror'
import { sql } from '@codemirror/lang-sql'
import { oneDark } from '@codemirror/theme-one-dark'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default {
  name: 'Exercises',
  components: {
    Codemirror
  },
  setup() {
    const userStore = useUserStore()
    const exercises = ref([])
    const difficulties = ref([])
    const themes = ref([])
    const userExercises = ref([])
    const loading = ref(false)
    const selectedExercise = ref(null)
    const userQuery = ref('')
    const submissionResult = ref(null)
    
    // Рефы для элементов
    const leftPanel = ref(null)
    const editorMain = ref(null)
    
    // Ширина левой панели
    const leftPanelWidth = ref(500)
    const isResizing = ref(false)
    
    // Пагинация
    const currentPage = ref(1)
    const pageSize = ref(25)
    
    // Фильтры
    const filters = ref({
      difficulty: '',
      theme: ''
    })
    
    // Сортировка
    const sortField = ref('exercises_id')
    const sortDirection = ref('asc')

    // Настройки CodeMirror
    const extensions = [sql(), oneDark]

    const user = computed(() => userStore.user)

    // Метод для принудительного закрытия редактора (будет вызываться из App.vue)
    const forceCloseEditor = () => {
      if (selectedExercise.value) {
        closeExercise()
      }
    }

    // Экспортируем метод, чтобы он был доступен извне
    const publicAPI = {
      forceCloseEditor
    }

    // Делаем API публичным
    defineExpose(publicAPI)

    // Функции для изменения размера панелей
    const startResize = (e) => {
      isResizing.value = true
      document.addEventListener('mousemove', handleResize)
      document.addEventListener('mouseup', stopResize)
      document.addEventListener('touchmove', handleResize)
      document.addEventListener('touchend', stopResize)
      
      e.preventDefault()
    }

    const handleResize = (e) => {
      if (!isResizing.value || !editorMain.value) return
      
      const containerRect = editorMain.value.getBoundingClientRect()
      let newWidth
      
      if (e.type === 'touchmove') {
        newWidth = e.touches[0].clientX - containerRect.left
      } else {
        newWidth = e.clientX - containerRect.left
      }
      
      const minWidth = 300
      const maxWidth = containerRect.width - 400
      
      if (newWidth >= minWidth && newWidth <= maxWidth) {
        leftPanelWidth.value = newWidth
      }
    }

    const stopResize = () => {
      isResizing.value = false
      document.removeEventListener('mousemove', handleResize)
      document.removeEventListener('mouseup', stopResize)
      document.removeEventListener('touchmove', handleResize)
      document.removeEventListener('touchend', stopResize)
    }

    const fetchDifficulties = async () => {
      try {
        const response = await axios.get(`${API_URL}/task-difficulties/`)
        difficulties.value = response.data
      } catch (error) {
        console.error('Error fetching difficulties:', error)
      }
    }

    const fetchThemes = async () => {
      try {
        const response = await axios.get(`${API_URL}/task-themes/`)
        themes.value = response.data
      } catch (error) {
        console.error('Error fetching themes:', error)
      }
    }

    const fetchExercises = async () => {
      loading.value = true
      try {
        const response = await axios.get(`${API_URL}/exercises/`)
        exercises.value = response.data
      } catch (error) {
        console.error('Error fetching exercises:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchUserExercises = async () => {
      if (!user.value) return
      
      try {
        const response = await axios.get(`${API_URL}/user-exercises/user/${user.value.user_id}`)
        userExercises.value = response.data
      } catch (error) {
        console.error('Error fetching user exercises:', error)
      }
    }

    // Применение фильтров
    const applyFilters = () => {
      currentPage.value = 1
    }

    // Сортировка
    const sortBy = (field) => {
      if (sortField.value === field) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortField.value = field
        sortDirection.value = 'asc'
      }
    }

    // Пагинация
    const updatePagination = () => {
      currentPage.value = 1
    }

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
      }
    }

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
      }
    }

    // Проверка выполнения задания
    const isCompleted = (exerciseId) => {
      return userExercises.value.some(ue => 
        ue.exercise_id === exerciseId && ue.completed
      )
    }

    // Класс для сложности
    const getDifficultyClass = (difficulty) => {
      if (!difficulty) return ''
      const name = difficulty.task_difficulty_name.toLowerCase()
      if (name.includes('легк')) return 'easy'
      if (name.includes('средн')) return 'medium'
      if (name.includes('сложн')) return 'hard'
      return ''
    }

    // Открытие задания в редакторе
    const openExercise = (exercise) => {
      selectedExercise.value = exercise
      userQuery.value = ''
      submissionResult.value = null
      
      // Загружаем предыдущее решение пользователя, если есть
      const userExercise = userExercises.value.find(
        ue => ue.exercise_id === exercise.exercises_id
      )
      if (userExercise) {
        userQuery.value = userExercise.user_query
      }

      // Сбрасываем ширину панели при открытии нового задания
      nextTick(() => {
        leftPanelWidth.value = 500
      })
    }

    // Закрытие редактора
    const closeExercise = () => {
      selectedExercise.value = null
      userQuery.value = ''
      submissionResult.value = null
    }

    // Очистка редактора
    const clearCode = () => {
      userQuery.value = ''
    }

    // Отправка решения
    const submitSolution = async () => {
      if (!user.value) {
        submissionResult.value = {
          type: 'error',
          message: 'Для отправки решений необходимо войти в систему'
        }
        return
      }

      if (!userQuery.value.trim()) {
        submissionResult.value = {
          type: 'error',
          message: 'Запрос не может быть пустым'
        }
        return
      }

      try {
        // Временная заглушка для проверки
        const isValid = await validateSolution(userQuery.value)
        
        const userExercise = {
          user_id: user.value.user_id,
          exercise_id: selectedExercise.value.exercises_id,
          completed: isValid,
          user_query: userQuery.value
        }

        await axios.post(`${API_URL}/user-exercises/`, userExercise)
        await fetchUserExercises()
        
        submissionResult.value = {
          type: isValid ? 'success' : 'warning',
          message: isValid 
            ? 'Задание выполнено успешно!' 
            : 'Задание отправлено, но требует доработки'
        }

      } catch (error) {
        console.error('Error submitting solution:', error)
        submissionResult.value = {
          type: 'error',
          message: 'Ошибка при отправке решения'
        }
      }
    }

    // Временная функция для проверки решения
    const validateSolution = async (query) => {
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(true)
        }, 1000)
      })
    }

    // Вычисляемые свойства
    const sortedExercises = computed(() => {
      return [...exercises.value].sort((a, b) => {
        let aValue, bValue

        switch (sortField.value) {
          case 'difficulty':
            aValue = a.difficulty?.task_difficulty_name || ''
            bValue = b.difficulty?.task_difficulty_name || ''
            break
          case 'completed':
            aValue = isCompleted(a.exercises_id)
            bValue = isCompleted(b.exercises_id)
            break
          default:
            aValue = a[sortField.value]
            bValue = b[sortField.value]
        }

        if (aValue < bValue) return sortDirection.value === 'asc' ? -1 : 1
        if (aValue > bValue) return sortDirection.value === 'asc' ? 1 : -1
        return 0
      })
    })

    const filteredExercises = computed(() => {
      return sortedExercises.value.filter(exercise => {
        const matchesDifficulty = !filters.value.difficulty || 
          exercise.task_difficulty_id == filters.value.difficulty
        const matchesTheme = !filters.value.theme || 
          exercise.task_theme_id == filters.value.theme
        return matchesDifficulty && matchesTheme
      })
    })

    const totalPages = computed(() => {
      return Math.ceil(filteredExercises.value.length / pageSize.value)
    })

    const displayedExercises = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filteredExercises.value.slice(start, end)
    })

    onMounted(() => {
      fetchDifficulties()
      fetchThemes()
      fetchExercises()
      fetchUserExercises()
    })

    return {
      exercises,
      difficulties,
      themes,
      loading,
      filters,
      sortField,
      sortDirection,
      pageSize,
      currentPage,
      selectedExercise,
      userQuery,
      submissionResult,
      extensions,
      leftPanel,
      editorMain,
      leftPanelWidth,
      isResizing,
      user,
      displayedExercises,
      filteredExercises,
      totalPages,
      startResize,
      handleResize,
      stopResize,
      applyFilters,
      sortBy,
      updatePagination,
      prevPage,
      nextPage,
      isCompleted,
      getDifficultyClass,
      openExercise,
      closeExercise,
      clearCode,
      submitSolution,
      forceCloseEditor
    }
  }
}
</script>