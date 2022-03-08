import axios from 'axios'

// 系统信息
export let sysInfo = () => { return axios.get('source/sysInfo') }

// 注册
export let userLogon = (data) => { return axios.post('users/logon', data) }

// 登录
export let userLogin = (data) => { return axios.post('users/login', data) };

// 短信验证码
export let smsCode = (mobile) => { return axios.get(`oauth/smsCode/${mobile}`) }

// 获取岗位和职级信息
export let getStaff = () => { return axios.get('source/staff') }