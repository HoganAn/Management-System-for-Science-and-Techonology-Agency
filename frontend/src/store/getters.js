const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  refresh: state => state.user.refresh,
  name: state => state.user.name,
  nickname: state => state.user.nickname
}
export default getters
