<template>
  <div>
    <!-- 搜索区域 -->
    <div id="search-scope">
      <!-- 搜索表单 -->
      <a-form-model ref="searchForm" layout="inline" :model="searchForm">
        <a-form-model-item label="模块名称" prop="name">
          <a-input placeholder="精确匹配" v-model="searchForm.name"></a-input>
        </a-form-model-item>
        <a-form-model-item label="自动化类名" prop="cls_name">
          <a-input
            placeholder="模糊匹配"
            v-model="searchForm.cls_name"
          ></a-input>
        </a-form-model-item>
        <a-form-model-item label="归属服务" prop="service">
          <a-select
            placeholder="请选择"
            v-model="searchForm.service"
            allowClear
          >
            <a-select-option
              v-for="item in services"
              :value="item.id"
              :key="item.id"
              >{{ item.name }}</a-select-option
            >
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="是否可用" prop="flag">
          <a-select v-model="searchForm.flag" placeholder="请选择" allowClear>
            <a-select-option :value="1">是</a-select-option>
            <a-select-option :value="0">否</a-select-option>
          </a-select>
        </a-form-model-item>
      </a-form-model>
      <!-- 操作按钮 -->
      <a-row id="button-scope">
        <a-col :span="12" style="text-align: left">
          <a-button
            type="primary"
            @click="
              () => {
                visible = true;
                isCreate = true;
              }
            "
            >创建模块</a-button
          >
        </a-col>
        <a-col :span="12" style="text-align: right">
          <a-button type="primary" @click="queryModules()">查询</a-button>
          <a-button @click="$refs.searchForm.resetFields()">重置</a-button>
        </a-col>
      </a-row>
      <!-- 创建模块弹窗 -->
      <a-modal
        id="modal"
        title="创建模块"
        :visible="visible"
        @ok="handleOk"
        @cancel="handleCancel"
        width="30em"
      >
        <a-form-model
          ref="moduleForm"
          :model="moduleForm"
          :wrapperCol="{ span: 18, offset: 3 }"
        >
          <a-form-model-item prop="name" required>
            <a-input v-model="moduleForm.name" placeholder="模块名称">
              <a-icon
                slot="prefix"
                type="medium"
                style="color: rgba(0, 0, 0, 0.25)"
              />
            </a-input>
          </a-form-model-item>
          <a-form-model-item prop="cls_name" required>
            <a-input v-model="moduleForm.cls_name" placeholder="自动化类名">
              <a-icon
                slot="prefix"
                type="block"
                style="color: rgba(0, 0, 0, 0.25)"
              />
            </a-input>
          </a-form-model-item>
          <a-form-model-item prop="service" required>
            <a-select placeholder="归属服务" v-model="moduleForm.service">
              <a-select-option
                v-for="item in services"
                :value="item.id"
                :key="item.id"
                >{{ item.name }}</a-select-option
              >
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="flag" required>
            <a-select placeholder="启用状态" v-model="moduleForm.flag">
              <a-select-option :value="1">启用</a-select-option>
              <a-select-option :value="0">禁用</a-select-option>
            </a-select>
          </a-form-model-item>
        </a-form-model>
      </a-modal>
      <!-- 删除服务弹窗 -->
      <a-modal
        title="删除模块"
        :visible="delete_visible"
        @ok="handleDeleteOk"
        @cancel="delete_visible = false"
        width="30em"
      >
        <span>目前不建议执行删除操作，是否继续？</span>
      </a-modal>
    </div>
    <!-- 表格区域 -->
    <div id="list-scope">
      <a-table
        :loading="loading"
        :columns="columns"
        :data-source="moduleList"
        :rowKey="
          (record) => {
            return record.id;
          }
        "
        :pagination="pagination"
      >
        <template slot="action" slot-scope="record">
          <a-button shape="circle" icon="edit" @click="updateModule(record)" />
          <a-button
            shape="circle"
            icon="delete"
            type="danger"
            style="margin-left: 0.5em"
            @click="
              () => {
                delete_visible = true;
                module_id = record.id;
              }
            "
          />
        </template>
        <template slot="flag" slot-scope="text">{{
          text == true ? "启用" : "禁用"
        }}</template>
      </a-table>
    </div>
  </div>
</template>
<script>
import {
  getAllService,
  getModuleList,
  createModule,
  updateModule,
  deleteModule,
} from "@/api";
import { pagination } from "@/components/base";
export default {
  data() {
    return {
      // 查询表单
      searchForm: {
        name: null,
        cls_name: null,
        service: undefined,
        flag: undefined,
      },

      // 可选服务
      services: [],

      // 创建模块弹窗
      visible: false,
      isCreate: true,
      moduleForm: {
        name: null,
        cls_name: null,
        service: undefined,
        flag: undefined,
      },

      // 表格
      loading: false,
      moduleList: [],
      columns: [
        {
          title: "ID",
          dataIndex: "id",
          align: "center",
          width: "5%",
        },
        {
          title: "名称",
          dataIndex: "name",
          align: "center",
          width: "15%",
        },
        {
          title: "自动化类名",
          dataIndex: "cls_name",
          align: "center",
          width: "15%",
        },
        {
          title: "归属服务",
          dataIndex: "service_name",
          align: "center",
          width: "15%",
        },
        {
          title: "状态",
          dataIndex: "flag",
          scopedSlots: { customRender: "flag" },
          align: "center",
          width: "5%",
        },
        {
          title: "创建人",
          dataIndex: "creator_name",
          align: "center",
          width: "15%",
        },
        {
          title: "创建时间",
          dataIndex: "create_time",
          align: "center",
          width: "15%",
        },
        {
          title: "操作",
          scopedSlots: { customRender: "action" },
          align: "center",
        },
      ],

      // 分页
      pagination: pagination(this.queryServices, ["20", "50", "100"]),

      // 删除任务变量
      delete_visible: false,
      module_id: null,
    };
  },
  methods: {
    // 弹窗确认回调
    handleOk() {
      this.$refs.moduleForm.validate((valid) => {
        if (valid) {
          if (this.isCreate) {
            createModule(this.moduleForm).then((res) => {
              this.$message.success(res.data.msg);
              this.visible = false;
              this.$refs.moduleForm.resetFields();
              this.queryModules();
            });
          } else {
            updateModule(this.moduleForm).then((res) => {
              this.$message.success(res.data.msg);
              this.visible = false;
              this.moduleForm = {
                name: null,
                cls_name: null,
                service: undefined,
                flag: undefined,
              };
              this.queryModules();
            });
          }
        }
      });
    },
    // 弹窗取消回调
    handleCancel() {
      this.visible = false;
      this.$refs.moduleForm.resetFields();
    },
    // 查询模块列表
    queryModules() {
      this.loading = true;
      this.searchForm.page = this.pagination.current;
      this.searchForm.page_size = this.pagination.pageSize;
      getModuleList(this.searchForm).then((res) => {
        this.moduleList = res.data.data;
        this.pagination.total = res.data.total;
        this.loading = false;
      });
    },
    // 更新模块
    updateModule(row) {
      this.visible = true;
      this.isCreate = false;
      this.moduleForm = JSON.parse(JSON.stringify(row));
    },
    // 删除模块
    handleDeleteOk() {
      deleteModule(this.module_id).then((res) => {
        this.$message.success(res.data.msg);
        this.queryModules();
      });
      this.delete_visible = false;
    },
  },
  created() {
    getAllService().then((res) => {
      this.services = res.data;
    });
    this.queryModules();
  },
};
</script>
<style scoped>
#search-scope {
  padding: 0.5em 0.5em;
  margin: 0.5em;
  background-color: lightgrey;
  border-radius: 0.3em;
}
.ant-form-inline .ant-form-item {
  width: 20em;
  text-align: right;
}
.ant-select,
.ant-input {
  width: 13em;
}
#button-scope {
  margin: 1em 1em 0;
}
#button-scope .ant-btn {
  margin: 0 1em;
}

#modal >>> .ant-select,
#modal >>> .ant-input {
  width: 20em;
}

#list-scope {
  margin: 0.5em;
  overflow: auto;
}
#list-scope >>> .ant-table-thead > tr > th {
  padding: 0.8em;
  color: white;
  background-color: lightslategrey;
}
#list-scope >>> .ant-table-tbody > tr > td {
  padding: 0.4em;
}
</style>