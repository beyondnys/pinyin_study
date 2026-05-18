<template>
  <div class="login-page page-container">
    <div class="login-card">
      <h1>🌈 游戏学习小课堂</h1>
      <p class="subtitle">{{ mode === 'login' ? '一起来练练吧！' : '创建你的学习账号' }}</p>

      <el-tabs v-model="mode" class="auth-tabs" stretch>
        <el-tab-pane label="登录" name="login" />
        <el-tab-pane label="注册" name="register" />
      </el-tabs>

      <!-- 登录 -->
      <el-form v-if="mode === 'login'" :model="loginForm" @submit.prevent="onLogin">
        <el-form-item>
          <el-input v-model="loginForm.username" placeholder="用户名" size="large" clearable />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            size="large"
            show-password
          />
        </el-form-item>
        <el-button type="primary" size="large" class="submit-btn" :loading="loading" native-type="submit" block>
          开始学习
        </el-button>
      </el-form>

      <!-- 注册 -->
      <el-form v-else :model="registerForm" @submit.prevent="onRegister">
        <el-form-item>
          <el-input v-model="registerForm.username" placeholder="用户名（2-64 位）" size="large" clearable />
        </el-form-item>
        <el-form-item>
          <el-input v-model="registerForm.nickname" placeholder="昵称（选填）" size="large" clearable />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="密码（至少 6 位）"
            size="large"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="确认密码"
            size="large"
            show-password
          />
        </el-form-item>
        <el-button type="primary" size="large" class="submit-btn" :loading="loading" native-type="submit" block>
          注册并登录
        </el-button>
      </el-form>

      <p class="hint">演示账号：student / student123</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const mode = ref<'login' | 'register'>('login')

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({
  username: '',
  nickname: '',
  password: '',
  confirmPassword: '',
})

async function onLogin() {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    await auth.login(loginForm.username.trim(), loginForm.password)
    ElMessage.success('登录成功')
    router.push('/games')
  } catch {
    /* request 已提示 */
  } finally {
    loading.value = false
  }
}

async function onRegister() {
  const username = registerForm.username.trim()
  if (!username) {
    ElMessage.warning('请输入用户名')
    return
  }
  if (username.length < 2) {
    ElMessage.warning('用户名至少 2 个字符')
    return
  }
  if (!registerForm.password || registerForm.password.length < 6) {
    ElMessage.warning('密码至少 6 位')
    return
  }
  if (registerForm.password !== registerForm.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  loading.value = true
  try {
    await auth.register(username, registerForm.password, registerForm.nickname.trim())
    ElMessage.success('注册成功')
    router.push('/games')
  } catch {
    /* request 已提示 */
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100dvh;
}
.login-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 24px;
  padding: clamp(24px, 6vw, 40px);
  box-shadow: 0 8px 32px rgba(74, 144, 226, 0.15);
  text-align: center;
}
h1 {
  font-size: clamp(22px, 5vw, 28px);
  color: #ff6b6b;
  margin-bottom: 8px;
}
.subtitle {
  color: #888;
  margin-bottom: 16px;
}
.auth-tabs {
  margin-bottom: 20px;
}
.auth-tabs :deep(.el-tabs__header) {
  margin-bottom: 0;
}
.submit-btn {
  width: 100%;
  min-height: 48px;
  border-radius: 12px;
  font-size: 16px;
}
.hint {
  margin-top: 16px;
  font-size: 12px;
  color: #aaa;
}
</style>
