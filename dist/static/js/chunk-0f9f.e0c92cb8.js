(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-0f9f"],{Is5O:function(t,e,r){"use strict";r.d(e,"s",function(){return s}),r.d(e,"q",function(){return i}),r.d(e,"e",function(){return l}),r.d(e,"n",function(){return u}),r.d(e,"c",function(){return c}),r.d(e,"h",function(){return p}),r.d(e,"j",function(){return m}),r.d(e,"k",function(){return b}),r.d(e,"o",function(){return f}),r.d(e,"d",function(){return v}),r.d(e,"p",function(){return g}),r.d(e,"i",function(){return h}),r.d(e,"b",function(){return _}),r.d(e,"m",function(){return y}),r.d(e,"g",function(){return w}),r.d(e,"a",function(){return F}),r.d(e,"l",function(){return O}),r.d(e,"f",function(){return j}),r.d(e,"t",function(){return k}),r.d(e,"r",function(){return $});var n=r("f0Pt"),o=r.n(n),a=r("t3Un"),d=o.a.create({baseURL:""});function s(t){return d({url:"/runtask/",method:"get",params:t})}function i(t){return o.a.create()({baseURL:"",url:"/initserver/",method:"get",params:t})}function l(t){return Object(a.a)({url:"/dashboard/",method:"get",params:t})}function u(t){return Object(a.a)({url:"/getserver/",method:"get",params:t})}function c(t){return Object(a.a)({url:"/addserver/",method:"post",params:t})}function p(t){return Object(a.a)({url:"/delserver/",method:"get",params:t})}function m(t){return Object(a.a)({url:"/editserver/",method:"get",params:t})}function b(t){return Object(a.a)({url:"/getallserver/",method:"get"})}function f(t){return Object(a.a)({url:"/getservice/",method:"get",params:t})}function v(t){return Object(a.a)({url:"/createtask/",method:"get",params:t})}function g(t){return Object(a.a)({url:"/gettask/",method:"get",params:t})}function h(t){return Object(a.a)({url:"/deltask/",method:"get",params:t})}function _(t){return Object(a.a)({url:"/addrepo/",method:"get",params:t})}function y(t){return Object(a.a)({url:"/getrepo/",method:"get"})}function w(t){return Object(a.a)({url:"/delrepo/",method:"get",params:t})}function F(t){return Object(a.a)({url:"/adddb/",method:"get",params:t})}function O(t){return Object(a.a)({url:"/getdb/",method:"get"})}function j(t){return Object(a.a)({url:"/deldb/",method:"get",params:t})}function k(t){return Object(a.a)({url:"/viewlog/",method:"get",params:t})}function $(t){return Object(a.a)({url:"/initstatus/",method:"get"})}},VqgU:function(t,e,r){"use strict";r.r(e);var n=r("Is5O"),o={data:function(){return{optionsService:[],optionsDbtype:[],loading:!1,db:[],addFormVisible:!1,addLoading:!1,addFormRules:{srv_type:[{required:!0,message:"请选择业务类型",trigger:"change"}],db_type:[{required:!0,message:"请选择数据库类型",trigger:"change"}],root_password:[{required:!0,message:"请输入root用户密码",trigger:"blur"},{pattern:/^(?=.*?[A-Z])(?=(.*[a-z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s).{8,}$/,message:"需要大小写，特殊字符和数字，至少8位"}],srv_password:[{required:!0,message:"请输入业务用户密码",trigger:"blur"},{pattern:/^(?=.*?[A-Z])(?=(.*[a-z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s).{8,}$/,message:"需要大小写，特殊字符和数字，至少8位"}]},addForm:{srv_type:"",db_type:"",root_password:"",srv_password:""}}},mounted:function(){this.handleGetDbInfo()},methods:{Service:function(){var t=this;Object(n.o)().then(function(e){t.optionsService=e.data})},handleGetDbInfo:function(){var t=this;this.loading=!0,Object(n.l)().then(function(e){t.loading=!1,t.db=e.data}).catch(function(){t.loading=!1})},getDbType:function(t){var e=this,r={service:t};Object(n.o)(r).then(function(t){e.optionsDbtype=t.data})},showadd:function(){this.addFormVisible=!0,this.Service()},handelDel:function(t,e){var r=this;this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(function(){var t={db_id:e.db_id};Object(n.f)(t).then(function(t){r.handleGetDbInfo()}).catch(function(){})})},onSubmit:function(){var t=this;this.$refs.addForm.validate(function(e){e&&t.$confirm("确认提交吗？","提示",{}).then(function(){t.addLoading=!0;var e={srv_type:t.addForm.srv_type,db_type:t.addForm.db_type,root_password:t.addForm.root_password,srv_password:t.addForm.srv_password};Object(n.a)(e).then(function(e){t.addLoading=!1,t.$refs.addForm.resetFields(),t.addFormVisible=!1,t.handleGetDbInfo()}).catch(function(e){t.addLoading=!1,t.$refs.addForm.resetFields(),t.addFormVisible=!1})})})}}},a=r("ZrdR"),d=Object(a.a)(o,function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"app-container"},[r("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[r("el-form",{attrs:{inline:!0}},[r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:t.showadd}},[t._v("添加")])],1)],1)],1),t._v(" "),[r("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],attrs:{data:t.db,"highlight-current-row":"",border:"",fit:"",stripe:""}},[r("el-table-column",{attrs:{type:"index",label:"序号",width:"80"}}),t._v(" "),r("el-table-column",{attrs:{prop:"srv_type",label:"服务名称",sortable:""}}),t._v(" "),r("el-table-column",{attrs:{prop:"db_type",label:"数据库类型",sortable:""}}),t._v(" "),r("el-table-column",{attrs:{prop:"root_password",label:"root用户密码",sortable:""}}),t._v(" "),r("el-table-column",{attrs:{prop:"srv_password",label:"业务用户密码",sortable:""}}),t._v(" "),r("el-table-column",{attrs:{label:"操作"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("el-button",{attrs:{type:"danger",size:"small"},on:{click:function(r){t.handelDel(e.$index,e.row)}}},[t._v("删除")])]}}])})],1)],t._v(" "),[r("el-dialog",{attrs:{visible:t.addFormVisible,"close-on-click-modal":!1,title:"添加数据库",width:"40%"},on:{"update:visible":function(e){t.addFormVisible=e}}},[r("el-form",{ref:"addForm",staticStyle:{width:"350px","margin-left":"30px"},attrs:{model:t.addForm,rules:t.addFormRules,"status-icon":"","label-width":"100px"}},[r("el-form-item",{attrs:{label:"选择服务:",prop:"srv_type"}},[r("el-select",{attrs:{filterable:"",clearable:"",size:"medium",placeholder:"请选择服务"},on:{change:function(e){t.getDbType(t.addForm.srv_type)}},model:{value:t.addForm.srv_type,callback:function(e){t.$set(t.addForm,"srv_type",e)},expression:"addForm.srv_type"}},t._l(t.optionsService,function(t){return r("el-option",{key:t.service,attrs:{label:t.service,value:t.service}})}))],1),t._v(" "),r("el-form-item",{attrs:{label:"选择数据库:",prop:"db_type"}},[r("el-select",{attrs:{filterable:"",clearable:"",size:"medium",placeholder:"请选择数据库"},model:{value:t.addForm.db_type,callback:function(e){t.$set(t.addForm,"db_type",e)},expression:"addForm.db_type"}},t._l(t.optionsDbtype,function(t){return r("el-option",{key:t.db_type,attrs:{label:t.db_type,value:t.db_type}})}))],1),t._v(" "),r("el-form-item",{attrs:{label:"root密码:",prop:"root_password"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:t.addForm.root_password,callback:function(e){t.$set(t.addForm,"root_password",e)},expression:"addForm.root_password"}})],1),t._v(" "),r("el-form-item",{attrs:{label:"业务密码:",prop:"srv_password"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:t.addForm.srv_password,callback:function(e){t.$set(t.addForm,"srv_password",e)},expression:"addForm.srv_password"}})],1),t._v(" "),r("el-form-item",[r("el-button",{attrs:{loading:t.addLoading,type:"primary"},on:{click:t.onSubmit}},[t._v("提交")]),t._v(" "),r("el-button",{on:{click:function(e){t.addFormVisible=!1}}},[t._v("取消")])],1)],1)],1)]],2)},[],!1,null,null,null);d.options.__file="db.vue";e.default=d.exports}}]);