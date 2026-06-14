import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/storage'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'Login', component: () => import('@/pages/Login.vue'), meta: { guest: true } },
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      children: [
        { path: '', redirect: '/games' },
        { path: 'games', name: 'Games', component: () => import('@/pages/GameList.vue') },
        {
          path: 'pinyin-select',
          name: 'PinyinSelect',
          component: () => import('@/pages/PinyinSelectGame.vue'),
        },
        { path: 'books', name: 'Books', component: () => import('@/pages/BookList.vue') },
        { path: 'practice/:bookId', name: 'Practice', component: () => import('@/pages/PracticeGame.vue') },
        { path: 'result/:recordId', name: 'Result', component: () => import('@/pages/PracticeResult.vue') },
        { path: 'wrong-questions', name: 'Wrong', component: () => import('@/pages/WrongQuestions.vue') },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const token = getToken()
  if (to.meta.guest) {
    if (token) next('/games')
    else next()
    return
  }
  if (!token) next('/login')
  else next()
})

export default router
