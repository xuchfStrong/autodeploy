(window.webpackJsonp=window.webpackJsonp||[]).push([["chunk-3df7"],{DDcb:function(t,e,r){},Is5O:function(t,e,r){"use strict";r.d(e,"s",function(){return l}),r.d(e,"q",function(){return s}),r.d(e,"e",function(){return d}),r.d(e,"n",function(){return u}),r.d(e,"c",function(){return c}),r.d(e,"h",function(){return m}),r.d(e,"j",function(){return p}),r.d(e,"k",function(){return f}),r.d(e,"o",function(){return h}),r.d(e,"d",function(){return b}),r.d(e,"p",function(){return g}),r.d(e,"i",function(){return v}),r.d(e,"b",function(){return _}),r.d(e,"m",function(){return F}),r.d(e,"g",function(){return w}),r.d(e,"a",function(){return k}),r.d(e,"l",function(){return j}),r.d(e,"f",function(){return O}),r.d(e,"t",function(){return x}),r.d(e,"r",function(){return y});var n=r("f0Pt"),o=r.n(n),i=r("t3Un"),a=o.a.create({baseURL:""});function l(t){return a({url:"/runtask/",method:"get",params:t})}function s(t){return o.a.create()({baseURL:"",url:"/initserver/",method:"get",params:t})}function d(t){return Object(i.a)({url:"/dashboard/",method:"get",params:t})}function u(t){return Object(i.a)({url:"/getserver/",method:"get",params:t})}function c(t){return Object(i.a)({url:"/addserver/",method:"post",params:t})}function m(t){return Object(i.a)({url:"/delserver/",method:"get",params:t})}function p(t){return Object(i.a)({url:"/editserver/",method:"get",params:t})}function f(t){return Object(i.a)({url:"/getallserver/",method:"get"})}function h(t){return Object(i.a)({url:"/getservice/",method:"get",params:t})}function b(t){return Object(i.a)({url:"/createtask/",method:"get",params:t})}function g(t){return Object(i.a)({url:"/gettask/",method:"get",params:t})}function v(t){return Object(i.a)({url:"/deltask/",method:"get",params:t})}function _(t){return Object(i.a)({url:"/addrepo/",method:"get",params:t})}function F(t){return Object(i.a)({url:"/getrepo/",method:"get"})}function w(t){return Object(i.a)({url:"/delrepo/",method:"get",params:t})}function k(t){return Object(i.a)({url:"/adddb/",method:"get",params:t})}function j(t){return Object(i.a)({url:"/getdb/",method:"get"})}function O(t){return Object(i.a)({url:"/deldb/",method:"get",params:t})}function x(t){return Object(i.a)({url:"/viewlog/",method:"get",params:t})}function y(t){return Object(i.a)({url:"/initstatus/",method:"get"})}},Kd3Y:function(t,e,r){"use strict";r.r(e);var n=r("6ZY3"),o=r.n(n),i=r("Is5O"),a={data:function(){return{filters:{ip:""},loading:!1,servers:[],sels:[],total:0,page:1,pagesize:10,addFormVisible:!1,addLoading:!1,addFormRules:{ip:[{required:!0,message:"请输入IP",trigger:"blur"}],hostname:[{required:!0,message:"请输入主机名",trigger:"blur"}],root_password:[{required:!0,message:"请输入root用户密码",trigger:"blur"}]},addForm:{ip:"",hostname:"",root_password:""},editFormVisible:!1,editLoading:!1,editFormRules:{name:[{required:!0,message:"请输入IP",trigger:"blur"}]},editForm:{ip:"",hostname:"",root_password:""}}},mounted:function(){this.getServer()},methods:{formatSex:function(t,e){return 1===t.sex?"男":0===t.sex?"女":"未知"},handleCurrentChange:function(t){this.page=t,this.getServer()},getServer:function(){var t=this;""!==this.filters.ip&&(this.page=1);var e={page:this.page,ip:this.filters.ip,pagesize:this.pagesize};this.loading=!0,Object(i.n)(e).then(function(e){t.total=e.data.total,t.servers=e.data.servers,t.loading=!1}).catch(function(e){t.loading=!1})},handleDel:function(t,e){var r=this;this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(function(){r.loading=!0;var t={host_id:e.host_id};Object(i.h)(t).then(function(t){r.loading=!1,r.getServer()}).catch(function(){r.loading=!1})})},selsChange:function(t){this.sels=t},batchRemove:function(){var t=this,e=this.sels.map(function(t){return t.host_id}).toString();this.$confirm("确认删除选中记录吗？","提示",{type:"warning"}).then(function(){t.loading=!0;var r={host_id:e};Object(i.h)(r).then(function(e){t.loading=!1,t.getServer()}).catch(function(){t.loading=!1})})},handleEdit:function(t,e){this.editFormVisible=!0,this.editForm=o()({},e)},editSubmit:function(){var t=this;this.$refs.editForm.validate(function(e){e&&t.$confirm("确认提交吗？","提示",{}).then(function(){t.editLoading=!0;var e=o()({},t.editForm);Object(i.j)(e).then(function(e){t.editLoading=!1,t.$refs.editForm.resetFields(),t.editFormVisible=!1,t.getServer()}).catch(function(e){t.editLoading=!1,t.$refs.editForm.resetFields(),t.editFormVisible=!1})})})},handleAdd:function(){this.addFormVisible=!0,this.addForm={ip:"",hostname:"",root_password:""}},addSubmit:function(){var t=this;this.$refs.addForm.validate(function(e){e&&t.$confirm("确认提交吗？","提示",{}).then(function(){t.addLoading=!0;var e=o()({},t.addForm);Object(i.c)(e).then(function(e){t.addLoading=!1,t.$refs.addForm.resetFields(),t.addFormVisible=!1,t.getServer()}).catch(function(e){t.addLoading=!1,t.$refs.addForm.resetFields(),t.addFormVisible=!1})})})}}},l=(r("U5ep"),r("ZrdR")),s=Object(l.a)(a,function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"app-container"},[r("el-col",{staticClass:"toolbar",staticStyle:{"padding-bottom":"0px"},attrs:{span:24}},[r("el-form",{attrs:{inline:!0,model:t.filters}},[r("el-form-item",[r("el-input",{attrs:{placeholder:"IP地址"},model:{value:t.filters.ip,callback:function(e){t.$set(t.filters,"ip",e)},expression:"filters.ip"}})],1),t._v(" "),r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:t.getServer}},[t._v("查询")])],1),t._v(" "),r("el-form-item",[r("el-button",{attrs:{type:"primary"},on:{click:t.handleAdd}},[t._v("添加")])],1)],1)],1),t._v(" "),[r("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],attrs:{data:t.servers,"highlight-current-row":"",border:"",fit:"",stripe:""},on:{"selection-change":t.selsChange}},[r("el-table-column",{attrs:{type:"selection",width:"55",align:"center"}}),t._v(" "),r("el-table-column",{attrs:{type:"index",label:"序号",width:"100",align:"center"}}),t._v(" "),r("el-table-column",{attrs:{prop:"hostname",label:"主机名",sortable:"",align:"center"}}),t._v(" "),r("el-table-column",{attrs:{prop:"ip",label:"IP地址",sortable:"",align:"center"}}),t._v(" "),r("el-table-column",{attrs:{label:"root密码",sortable:"",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(t._s(e.row.root_password))]}}])}),t._v(" "),r("el-table-column",{attrs:{prop:"host_id",label:"主机ID",width:"100",sortable:"",align:"center"}}),t._v(" "),r("el-table-column",{attrs:{label:"操作",width:"150",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[r("el-button",{attrs:{size:"small"},on:{click:function(r){t.handleEdit(e.$index,e.row)}}},[t._v("修改")]),t._v(" "),r("el-button",{attrs:{type:"danger",size:"small"},on:{click:function(r){t.handleDel(e.$index,e.row)}}},[t._v("删除")])]}}])})],1)],t._v(" "),r("el-col",{staticClass:"toolbar toolbar-container",attrs:{span:24}},[r("el-button",{attrs:{disabled:0===t.sels.length,type:"danger"},on:{click:t.batchRemove}},[t._v("批量删除")]),t._v(" "),r("el-pagination",{staticStyle:{float:"right"},attrs:{total:t.total,"page-size":t.pagesize,layout:"prev, pager, next"},on:{"current-change":t.handleCurrentChange}})],1),t._v(" "),[r("el-dialog",{attrs:{visible:t.addFormVisible,"close-on-click-modal":!1,title:"添加",width:"40%"},on:{"update:visible":function(e){t.addFormVisible=e}}},[r("el-form",{ref:"addForm",staticStyle:{width:"350px","margin-left":"30px"},attrs:{model:t.addForm,rules:t.addFormRules,"status-icon":"","label-width":"90px"}},[r("el-form-item",{attrs:{label:"IP地址:",prop:"ip"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:t.addForm.ip,callback:function(e){t.$set(t.addForm,"ip",e)},expression:"addForm.ip"}})],1),t._v(" "),r("el-form-item",{attrs:{label:"主机名:",prop:"hostname"}},[r("el-input",{model:{value:t.addForm.hostname,callback:function(e){t.$set(t.addForm,"hostname",e)},expression:"addForm.hostname"}})],1),t._v(" "),r("el-form-item",{attrs:{label:"root密码:",prop:"root_password"}},[r("el-input",{model:{value:t.addForm.root_password,callback:function(e){t.$set(t.addForm,"root_password",e)},expression:"addForm.root_password"}})],1),t._v(" "),r("el-form-item",[r("el-button",{attrs:{loading:t.addLoading,type:"primary"},on:{click:t.addSubmit}},[t._v("提交")]),t._v(" "),r("el-button",{on:{click:function(e){t.addFormVisible=!1}}},[t._v("取消")])],1)],1)],1)],t._v(" "),[r("el-dialog",{attrs:{visible:t.editFormVisible,"close-on-click-modal":!1,title:"修改",width:"40%"},on:{"update:visible":function(e){t.editFormVisible=e}}},[r("el-form",{ref:"editForm",staticStyle:{width:"350px","margin-left":"30px"},attrs:{model:t.editForm,rules:t.addFormRules,"status-icon":"","label-width":"90px"}},[r("el-form-item",{attrs:{label:"IP地址:",prop:"ip"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:t.editForm.ip,callback:function(e){t.$set(t.editForm,"ip",e)},expression:"editForm.ip"}})],1),t._v(" "),r("el-form-item",{attrs:{label:"主机名:",prop:"hostname"}},[r("el-input",{model:{value:t.editForm.hostname,callback:function(e){t.$set(t.editForm,"hostname",e)},expression:"editForm.hostname"}})],1),t._v(" "),r("el-form-item",{attrs:{label:"root密码:",prop:"root_password"}},[r("el-input",{model:{value:t.editForm.root_password,callback:function(e){t.$set(t.editForm,"root_password",e)},expression:"editForm.root_password"}})],1),t._v(" "),r("el-form-item",[r("el-button",{attrs:{loading:t.editLoading,type:"primary"},on:{click:t.editSubmit}},[t._v("提交")]),t._v(" "),r("el-button",{on:{click:function(e){t.editFormVisible=!1}}},[t._v("取消")])],1)],1)],1)]],2)},[],!1,null,"8fbe2d3e",null);s.options.__file="server.vue";e.default=s.exports},U5ep:function(t,e,r){"use strict";var n=r("DDcb");r.n(n).a}}]);