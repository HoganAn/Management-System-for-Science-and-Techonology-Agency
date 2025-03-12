import request from '@/utils/request'

export function getCaseList(params) {
  return request({
    url: '/case',
    method: 'get',
    params
  })
}

export function getCaseDetail(caseId) {
  return request({
    url: '/case/' + caseId.toString(),
    method: 'get'
  })
}

export function postCaseDetail(data) {
  return request({
    url: '/case/',
    method: 'post',
    data
  })
}

export function patchCaseDetail(caseId, data) {
  return request({
    url: '/case/' + caseId.toString() + '/',
    method: 'patch',
    data
  })
}

export function deleteCaseItem(caseId) {
  return request({
    url: '/case/' + caseId.toString(),
    method: 'delete'
  })
}

export function getServiceList(caseId, params) {
  return request({
    url: '/case/' + caseId.toString() + '/service/',
    method: 'get',
    params
  })
}

export function getServDetail(caseId, servId) {
  return request({
    url: '/case/' + caseId.toString() + '/service/' + servId.toString(),
    method: 'get'
  })
}

export function postServDetail(caseId, data) {
  return request({
    url: '/case/' + caseId.toString() + '/service/',
    method: 'post',
    data
  })
}

export function patchServDetail(caseId, servId, data) {
  return request({
    url: '/case/' + caseId.toString() + '/service/' + servId.toString() + '/',
    method: 'patch',
    data
  })
}

export function deleteServItem(caseId, servId) {
  return request({
    url: '/case/' + caseId.toString() + '/service/' + servId.toString(),
    method: 'delete'
  })
}

export function getCaseDocList(params) {
  return request({
    url: '/case-doc/',
    method: 'get',
    params
  })
}

export function deleteDocItem(id) {
  return request({
    url: '/case-doc/' + id.toString() + '/',
    method: 'delete'
  })
}

export function getCaseDoc(id) {
  return request({
    url: '/case-doc/' + id.toString() + '/download/',
    method: 'get',
    responseType: 'blob'
  })
}

export function getServDocList(params) {
  return request({
    url: '/serv-doc/',
    method: 'get',
    params
  })
}

export function deleteServDocItem(id) {
  return request({
    url: '/serv-doc/' + id.toString() + '/',
    method: 'delete'
  })
}

export function getServDoc(id) {
  return request({
    url: '/serv-doc/' + id.toString() + '/download/',
    method: 'get',
    responseType: 'blob'
  })
}
