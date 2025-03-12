import Cookies from 'js-cookie'

const TokenKey = 'token'
const RefreshToken = 'refresh'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function getRefresh() {
  return Cookies.get(RefreshToken)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function setRefresh(refresh) {
  return Cookies.set(RefreshToken, refresh)
}

export function removeToken() {
  Cookies.remove(TokenKey)
  Cookies.remove(RefreshToken)
}
