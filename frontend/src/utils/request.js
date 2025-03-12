import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken, getRefresh, setToken } from '@/utils/auth'
import NProgress from '@/utils/progress'
import { refreshToken } from '@/api/user'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_URL + process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    NProgress.start()

    if (store.getters.token) {
      // let each request carry token
      config.headers['Authorization'] = 'JWT ' + getToken()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    NProgress.done()
    return response
  },
  error => {
    error = error.response
    if (error.status === 401) {
      const refresh = getRefresh()
      if (error.config.url.includes('/auth/jwt/refresh')) {
        NProgress.done()
        Message({
          message: '登录凭证已过期，请重新登录',
          type: 'warning',
          duration: 1000
        })
          .then(() => {
            store.dispatch('user/resetToken')
              .then(() => {
                location.reload()
              })
          })
      } else {
        return refreshToken({ refresh: refresh })
          .then(response => {
            const { access } = response.data
            setToken(access)
            store.commit('user/SET_TOKEN', access)
            error.config.headers.Authorization = 'JWT ' + getToken()
            return service(error.config)
          })
      }
    } else {
      if (error.config.url.includes('/auth/jwt/refresh')) {
        Message({
          message: '用户名或密码错误',
          type: 'error',
          duration: 2000
        })
      } else {
        Message({
          message: error.message,
          type: 'error',
          duration: 2 * 1000
        })
      }
    }

    NProgress.done()
    return Promise.reject(error)
  }
)

export default service
