import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/auth/jwt/create',
    method: 'post',
    data
  })
}

export function refreshToken(data) {
  return request({
    url: '/auth/jwt/refresh',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/auth/users/me',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
