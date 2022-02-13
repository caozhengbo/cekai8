import axios from 'axios'
import store from '../store/state'
import router from '../router'
import {Message} from 'element-ui';



export const baseUrl = "http://110.42.184.157";
// export const baseUrl = "http://192.168.145.128:8000";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = baseUrl;

axios.interceptors.request.use(function (config) {
    if (config.url.indexOf("/api/testrunner/project/?cursor=") !== -1 ) {
    }
    else if (!config.url.startsWith("/api/user/")) {
        config.url = config.url + "?token=" + store.token;
    }
    return config;
}, function (error) {
    return Promise.reject(error);
});

axios.interceptors.response.use(function (response) {

    return response;
}, function (error) {
    try {
        if (error.response.status === 401) {
            router.replace({
                name: 'Login'
            })
        }

        if (error.response.status === 500) {
            Message.error({
                message: '服务器内部异常, 请检查',
                duration: 1000
            })
        }
    }
    catch (e) {
        Message.error({
            message: '服务器连接超时，请重试',
            duration: 1000
        })
    }
});

// user api
export const register = params => {
	//application/json
	//multipart/form-data
    return axios.post('/api/user/register/', params).then(res => res.data)
};

export const login = params => {
    return axios.post('/api/user/login/', params).then(res => res.data)
};
//uicase
export const adduicase = params => {
    return axios.post('/api/testrunner/uicase/', params).then(res => res.data)
};
export const getuicase = params => {
    return axios.get('/api/testrunner/uicase/', params).then(res => res.data)
};
export const getuicaseSingle = url => {
    return axios.get('/api/testrunner/uicase/' + url + '/').then(res => res.data)
};
export const deluicase = url => {
    return axios.delete('/api/testrunner/uicase/' + url + '/').then(res => res.data)
};
export const delAlluicase = params => {
    return axios.delete('/api/testrunner/uicase/', params).then(res => res.data)
};
export const updateuicase = (url,params) => {
    return axios.patch('/api/testrunner/uicase/' + url + '/',params).then(res => res.data)
};
export const copyuicase = (url, params) => {
    return axios.post('/api/testrunner/uicase/' + url + '/', params).then(res => res.data)
};
export const runuicase = (params) => {
    return axios.post('/api/testrunner/run_uicase/', params).then(res => res.data)
};
export const runUIcaseByPk = (url, params) => {
    return axios.get('/api/testrunner/run_uicase_pk/' + url + '/',params).then(res => res.data)
};
export const geuicasePaginationBypage = params => {
    return axios.get('/api/testrunner/uicase/', params).then(res => res.data)
};

export const runUIcaseTree = params => {
    return axios.post('/api/testrunner/run_uicase_tree/', params).then(res => res.data)
};
//获取ui测试计划列表
export const UItestPlanList = params => {
    return axios.get('/api/testrunner/uitest/', params).then(res => res.data)
};
export const getUITestPaginationBypage = params => {
    return axios.get('/api/testrunner/uitest/', params).then(res => res.data)
};
export const addUITestPlan = params => {
    return axios.post('/api/testrunner/uitest/', params).then(res => res.data)
};

export const updateUITestPlan = (url, params) => {
    return axios.patch('/api/testrunner/uitest/' + url + '/', params).then(res => res.data)
};
export const editUITest = url => {
    return axios.get('/api/testrunner/uitestplanstep/' + url + '/').then(res => res.data)
};
export const copyUITest = (url, params) => {
    return axios.post('/api/testrunner/uitest/' + url + '/', params).then(res => res.data)
};

export const deleteUITest = url => {
    return axios.delete('/api/testrunner/uitest/' + url + '/').then(res => res.data)
};
export const delAllUITest = params => {
    return axios.delete('/api/testrunner/uitest/', params).then(res => res.data)
};
export const runSingleTestPlanSuite = params => {
    return axios.post('/api/testrunner/run_testplansuite/', params).then(res => res.data)
};
export const runTestPlanByPk = (url, params) => {
    return axios.get('/api/testrunner/run_testplansuite_pk/' + url + '/', params).then(res => res.data)
};
export const runUIPlanSuiteTree = params => {
    return axios.post('/api/testrunner/run_testplansuite_tree/', params).then(res => res.data)
};
// testrunner api
export const addProject = params => {
    return axios.post('/api/testrunner/project/', params).then(res => res.data)
};

export const deleteProject = config => {
    return axios.delete('/api/testrunner/project/', config).then(res => res.data)
};

export const getProjectList = params => {
    return axios.get('/api/testrunner/project/').then(res => res.data)
};

export const getProjectDetail = pk => {
    return axios.get('/api/testrunner/project/' + pk + '/').then(res => res.data)
};

export const getPagination = url => {
    return axios.get(url).then(res => res.data)
};

export const updateProject = params => {
    return axios.patch('/api/testrunner/project/', params).then(res => res.data)
};

export const getDebugtalk = url => {
    return axios.get('/api/testrunner/debugtalk/' + url + '/').then(res => res.data)
};

export const updateDebugtalk = params => {
    return axios.patch('/api/testrunner/debugtalk/', params).then(res => res.data)
};

export const runDebugtalk = params => {
    return axios.post('/api/testrunner/debugtalk/', params).then(res => res.data)
};

export const getTree = (url, params) => {
    return axios.get('/api/testrunner/tree/' + url + '/', params).then(res => res.data)
};

export const updateTree = (url, params) => {
    return axios.patch('/api/testrunner/tree/' + url + '/', params).then(res => res.data)
};

export const uploadFile = url => {
    return baseUrl + '/api/testrunner/file/?token=' + store.token
};

export const downloadTestdata = params => {
    return axios.post('/api/testrunner/download/',params,{responseType:'blob' })
};

export const addAPI = params => {
    return axios.post('/api/testrunner/api/', params).then(res => res.data)
};

export const updateAPI = (url, params) => {
    return axios.patch('/api/testrunner/api/' + url + '/', params).then(res => res.data)
};

export const apiList = params => {
    return axios.get('/api/testrunner/api/', params).then(res => res.data)
};

export const delAPI = url => {
    return axios.delete('/api/testrunner/api/' + url + '/').then(res => res.data)
};

export const delAllAPI = params => {
    return axios.delete('/api/testrunner/api/', params).then(res => res.data)
};

export const getAPISingle = url => {
    return axios.get('/api/testrunner/api/' + url + '/').then(res => res.data)
};



export const getPaginationBypage = params => {
    return axios.get('/api/testrunner/api/', params).then(res => res.data)
};

export const deleteDataBase = pk =>{
    return axios.delete('/api/testrunner/databaseconfig/'+pk+'/').then(res => res.data)
}
export const updateDataBase = (pk,params) =>{
    return axios.put('/api/testrunner/databaseconfig/'+pk+'/',params).then(res =>res.data)
}
export const addDataBase =params =>{
    return axios.post('/api/testrunner/databaseconfig/',params).then(res=>res.data)
}
export const getDataBaseList =(pk,params) =>{
    return axios.get('/api/testrunner/databaseconfig/'+pk+'/',params).then(res=>res.data)
}
export const addTestCase = params => {
    return axios.post('/api/testrunner/test/', params).then(res => res.data)
};

export const updateTestCase = (url, params) => {
    return axios.patch('/api/testrunner/test/' + url + '/', params).then(res => res.data)
};

export const testList = params => {
    return axios.get('/api/testrunner/test/', params).then(res => res.data)
};

export const deleteTest = url => {
    return axios.delete('/api/testrunner/test/' + url + '/').then(res => res.data)
};

export const delAllTest = params => {
    return axios.delete('/api/testrunner/test/', params).then(res => res.data)
};

export const coptTest = (url, params) => {
    return axios.post('/api/testrunner/test/' + url + '/', params).then(res => res.data)
};

export const editTest = url => {
    return axios.get('/api/testrunner/teststep/' + url + '/').then(res => res.data)
};

export const getTestPaginationBypage = params => {
    return axios.get('/api/testrunner/test/', params).then(res => res.data)
};
export const gettagcount = params => {
    return axios.get('/api/testrunner/gettagcount/', params).then(res => res.data)
};
export const getreporttail = params => {
    return axios.get('/api/testrunner/getreporttail/', params).then(res => res.data)
};
export const addConfig = params => {
    return axios.post('/api/testrunner/config/', params).then(res => res.data)
};

export const updateConfig = (url, params) => {
    return axios.patch('/api/testrunner/config/' + url + '/', params).then(res => res.data)
};


export const configList = params => {
    return axios.get('/api/testrunner/config/', params).then(res => res.data)
};

export const copyConfig = (url, params) => {
    return axios.post('/api/testrunner/config/' + url + '/', params).then(res => res.data)
};

export const copyAPI = (url, params) => {
    return axios.post('/api/testrunner/api/' + url + '/', params).then(res => res.data)
};

export const deleteConfig = url => {
    return axios.delete('/api/testrunner/config/' + url + '/').then(res => res.data)
};
export const delAllConfig = params => {
    return axios.delete('/api/testrunner/config/', params).then(res => res.data)
};

export const getConfigPaginationBypage = params => {
    return axios.get('/api/testrunner/config/', params).then(res => res.data)
};

export const getAllConfig = url => {
    return axios.get('/api/testrunner/config/' + url + '/').then(res => res.data)
};


export const runSingleAPI = params => {
    return axios.post('/api/testrunner/run_api/', params).then(res => res.data)
};

export const runAPIByPk = (url, params) => {
    return axios.get('/api/testrunner/run_api_pk/' + url + '/', params).then(res => res.data)
};

export const runAPITree = params => {
    return axios.post('/api/testrunner/run_api_tree/', params).then(res => res.data)
};

export const runSingleTestSuite = params => {
    return axios.post('/api/testrunner/run_testsuite/', params).then(res => res.data)
};

export const runSingleTest = params => {
    return axios.post('/api/testrunner/run_test/', params).then(res => res.data)
};

export const runTestByPk = (url, params) => {
    return axios.get('/api/testrunner/run_testsuite_pk/' + url + '/', params).then(res => res.data)
};

export const runSuiteTree = params => {
    return axios.post('/api/testrunner/run_suite_tree/', params).then(res => res.data)
};

export const addVariables = params => {
    return axios.post('/api/testrunner/variables/', params).then(res => res.data)
};

export const variablesList = params => {
    return axios.get('/api/testrunner/variables/', params).then(res => res.data)
};

export const getVariablesPaginationBypage = params => {
    return axios.get('/api/testrunner/variables/', params).then(res => res.data)
};


export const updateVariables = (url, params) => {
    return axios.patch('/api/testrunner/variables/' + url + '/', params).then(res => res.data)
};

export const deleteVariables = url => {
    return axios.delete('/api/testrunner/variables/' + url + '/').then(res => res.data)
};

export const delAllVariabels = params => {
    return axios.delete('/api/testrunner/variables/', params).then(res => res.data)
};

export const reportList = params => {
    return axios.get('/api/testrunner/reports/', params).then(res => res.data)
};
export const uireportList = params => {
    return axios.get('/api/testrunner/uireports/', params).then(res => res.data)
};
export const deleteReports = (url,params) => {
    return axios.delete('/api/testrunner/reports/' + url + '/',params)
};

export const getReportsPaginationBypage = params => {
    return axios.get('/api/testrunner/reports/', params).then(res => res.data)
};
export const getUIReportsPaginationBypage = params => {
    return axios.get('/api/testrunner/uireports/', params).then(res => res.data)
};
export const getUIReportsdetail = (url,params) => {
    return axios.get('/api/testrunner/uireports/'+url+'/', params).then(res => res.data)
};
export const deleteUIReports = (url, params) => {
    return axios.delete('/api/testrunner/uireports/' + url + '/', params)
};
export const deleteAllUIReports = (url, params) => {
    return axios({ url: '/api/testrunner/uireports/', method: 'delete', params: params, data: data })
};
export const delAllReports = (data,params) => {
    return axios({url:'/api/testrunner/reports/', method: 'delete',params:params, data:data})
};

export const watchSingleReports = (url,params) => {
    return axios.get('/api/testrunner/reports/' + url + '/', params)
};
export const addTask = (params, data) => {
    return axios({url:'/api/testrunner/schedule/', method: 'POST', params:params, data:data})
};

export const copySchedule = (params, data)  => {
    return axios({url:'/api/testrunner/schedule/', method: 'POST', params:params, data:data})
};

export const updateTask = (url, params, data) => {
    return axios({url:'/api/testrunner/schedule/' + url + '/', method: 'PATCH', params:params, data:data})
};

export const taskList = params => {
    return axios.get('/api/testrunner/schedule/', params).then(res => res.data)
};
export const getTaskPaginationBypage = params => {
    return axios.get('/api/testrunner/schedule/', params).then(res => res.data)
};
export const deleteTasks = (url,params) => {
    return axios.delete('/api/testrunner/schedule/' + url + '/',params)
};
export const deleteSelectTasks = (params, data) => {
    return axios.delete('/api/testrunner/schedule/-1/', {params:params, data:data})
};
// export const addTask = params => {
//     return axios.post('/api/testrunner/schedule/', params).then(res => res.data)
// };
// export const taskList = params => {
//     return axios.get('/api/testrunner/schedule/', params).then(res => res.data)
// };
// export const getTaskPaginationBypage = params => {
//     return axios.get('/api/testrunner/schedule/', params).then(res => res.data)
// };
// export const deleteTasks = url => {
//     return axios.delete('/api/testrunner/schedule/' + url + '/').then(res => res.data)
// };

export const addHostIP = params => {
    return axios.post('/api/testrunner/host_ip/', params).then(res => res.data)
};

export const hostList = params => {
    return axios.get('/api/testrunner/host_ip/', params).then(res => res.data)
};

export const updateHost = (url, params) => {
    return axios.patch('/api/testrunner/host_ip/' + url + '/', params).then(res => res.data)
};

export const deleteHost = url => {
    return axios.delete('/api/testrunner/host_ip/' + url + '/').then(res => res.data)
};

export const getHostPaginationBypage = params => {
    return axios.get('/api/testrunner/host_ip/', params).then(res => res.data)
};

export const getAllHost = url => {
    return axios.get('/api/testrunner/host_ip/' + url + '/').then(res => res.data)
};
export const addPycode = (data,params) => {
    return axios({url:'/api/testrunner/pycode/', method:'POST', data:data, params:params})
};

export const deletePycode = (url, params) => {
    return axios.delete('/api/testrunner/pycode/' + url + '/', params)
};

export const delAllPycode = (data, params) => {
    return axios.delete('/api/testrunner/pycode/', {data, params})
};

export const getPycodeList = params => {
    return axios.get('/api/testrunner/pycode/', params)
};

export const getPycodeListPaginationBypage = params => {
    return axios.get('/api/testrunner/pycode/', params)
};

export const getPycode = (url, params) => {
    return axios.get('/api/testrunner/pycode/' + url + '/', params)
};

export const runPycode = (url, params) => {
    return axios.get('/api/testrunner/runpycode/' + url + '/', params)
};

export const updatePycode = (url, params, data) => {
    return axios({url:'/api/testrunner/pycode/' + url + '/', method:'PATCH', params:params,data:data})
};

export const runScheduleTest = url => {
    return axios.get('/api/testrunner/run_schedule_test/' + url + '/')
};

export const getTaskMetaDataList = params => {
    return axios.get('/api/testrunner/taskmeta/', params)
};
export const synchronizationapi = params => {
    return axios.post('/api/testrunner/synchronization_api/', params)
};
export const gettokenmsg = params => {
    return axios.post('/api/testrunner/gettokenmsg/', params)
};
