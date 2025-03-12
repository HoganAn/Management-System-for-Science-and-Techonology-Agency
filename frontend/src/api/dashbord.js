import request from '@/utils/request'

export function getUserKeywords() {
  return request({
    url: '/user-keywords/',
    method: 'get'
  })
}

export function getTypeList() {
  return request({
    url: '/service-type-statistics/',
    method: 'get'
  })
}

export function getUserStats() {
  return request({
    url: '/stats/',
    method: 'get'
  })
}
