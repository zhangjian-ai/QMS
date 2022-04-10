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

// 获取主页菜单配置
export let getMenu = () => { return axios.get('source/menu') }

// 获取协议信息
export let getProto = () => { return axios.get('source/proto') }

// 创建服务
export let createService = data => { return axios.post('service', data) }

// 更新服务
export let updateService = data => { return axios.put('service', data) }

// 删除服务
export let deleteService = id => { return axios.delete('service', { data: { id: id } }) }

// 查询服务列表
export let getServiceList = data => { return axios.get('service', { params: data }) }

// 获取所有服务
export let getAllService = () => { return axios.get('allService') }

// 创建模块
export let createModule = data => { return axios.post('module', data) }

// 更新模块
export let updateModule = data => { return axios.put('module', data) }

// 删除模块
export let deleteModule = id => { return axios.delete('module', { data: { id: id } }) }

// 查询模块列表
export let getModuleList = data => { return axios.get('module', { params: data }) }