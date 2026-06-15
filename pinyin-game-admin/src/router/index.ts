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
        { path: 'dashboard', component: () => import('@/pages/Dashboard.vue'), meta: { title: '仪表盘' } },
        { path: 'users', component: () => import('@/pages/UserList.vue'), meta: { title: '用户管理' } },
        { path: 'words', component: () => import('@/pages/WordList.vue'), meta: { title: '字库' } },
        { path: 'books', component: () => import('@/pages/BookList.vue'), meta: { title: '拼音练习册' } },
        { path: 'questions/:bookId', component: () => import('@/pages/QuestionList.vue'), meta: { title: '练习册题目' } },
        { path: 'import-tasks', component: () => import('@/pages/ImportTask.vue'), meta: { title: '拼音文本导入' } },
        { path: 'word-books', component: () => import('@/pages/WordBookList.vue'), meta: { title: '词语词库' } },
        {
          path: 'word-questions/:bookId',
          component: () => import('@/pages/WordQuestionList.vue'),
          meta: { title: '词语管理' },
        },
        {
          path: 'practice-records',
          component: () => import('@/pages/PracticeRecordList.vue'),
          meta: { title: '学习记录 · 拼音练习' },
        },
        {
          path: 'word-match-records',
          component: () => import('@/pages/WordMatchRecordList.vue'),
          meta: { title: '学习记录 · 词语连连看' },
        },
        { path: 'wrong-questions', component: () => import('@/pages/WrongQuestionList.vue'), meta: { title: '错题' } },
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
