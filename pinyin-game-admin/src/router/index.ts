import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/storage'

const router = createRouter({
  history: createWebHistory('/admin/'),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/pages/Login.vue'),
      meta: { guest: true },
    },
    {
      path: '/',
      component: () => import('@/layouts/AdminLayout.vue'),
      redirect: '/dashboard',
      children: [
        { path: 'dashboard', component: () => import('@/pages/Dashboard.vue') },
        { path: 'users', component: () => import('@/pages/UserList.vue') },
        { path: 'words', component: () => import('@/pages/WordList.vue') },
        { path: 'books', component: () => import('@/pages/BookList.vue') },
        { path: 'questions/:bookId', component: () => import('@/pages/QuestionList.vue') },
        { path: 'import-tasks', component: () => import('@/pages/ImportTask.vue') },
        { path: 'practice-records', component: () => import('@/pages/PracticeRecordList.vue') },
        { path: 'wrong-questions', component: () => import('@/pages/WrongQuestionList.vue') },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const token = getToken()
  if (to.meta.guest) {
    token ? next('/dashboard') : next()
    return
  }
  token ? next() : next('/login')
})

export default router
