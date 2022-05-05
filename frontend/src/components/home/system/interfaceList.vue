<template>
  <div>
    <!-- 搜索区域 -->
    <div id="search-scope">
      <!-- 搜索表单 -->
      <a-form-model ref="searchForm" layout="inline" :model="searchForm">
        <a-form-model-item label="接口名称" prop="name">
          <a-input placeholder="精确匹配" v-model="searchForm.name"></a-input>
        </a-form-model-item>
        <a-form-model-item label="URI" prop="uri">
          <a-input
            placeholder="模糊匹配"
            v-model="searchForm.uri"
          ></a-input>
        </a-form-model-item>
        <a-form-model-item label="归属模块" prop="module">
          <a-select
            placeholder="请选择"
            v-model="searchForm.module"
            allowClear
          >
            <a-select-option
              v-for="item in modules"
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
            >新增接口</a-button
          >
        </a-col>
        <a-col :span="12" style="text-align: right">
          <a-button type="primary" @click="queryInterfaces()">查询</a-button>
          <a-button @click="$refs.searchForm.resetFields()">重置</a-button>
        </a-col>
      </a-row>
      <!-- 创建模块弹窗 -->
      <a-modal
        id="modal"
        title="新增接口"
        :visible="visible"
        @ok="handleOk"
        @cancel="handleCancel"
        width="30em"
      >
        <a-form-model
          ref="interfaceForm"
          :model="interfaceForm"
          :wrapperCol="{ span: 18, offset: 3 }"
        >
          <a-form-model-item prop="name" required>
            <a-input v-model="interfaceForm.name" placeholder="接口名称">
              <a-icon
                slot="prefix"
                type="italic"
                style="color: rgba(0, 0, 0, 0.25)"
              />
            </a-input>
          </a-form-model-item>
          <a-form-model-item prop="uri" required>
            <a-input v-model="interfaceForm.uri" placeholder="URI">
              <a-icon
                slot="prefix"
                type="shrink"
                style="color: rgba(0, 0, 0, 0.25)"
              />
            </a-input>
          </a-form-model-item>
          <a-form-model-item prop="module" required>
            <a-select placeholder="归属模块" v-model="interfaceForm.module">
              <a-select-option
                v-for="item in modules"
                :value="item.id"
                :key="item.id"
                >{{ item.name }}</a-select-option
              >
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="flag" required>
            <a-select placeholder="启用状态" v-model="interfaceForm.flag">
              <a-select-option :value="1">启用</a-select-option>
              <a-select-option :value="0">禁用</a-select-option>
            </a-select>
          </a-form-model-item>
        </a-form-model>
      </a-modal>
      <!-- 删除服务弹窗 -->
      <a-modal
        title="删除接口"
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
        :data-source="interfaceList"
        :rowKey="
          (record) => {
            return record.id;
          }
        "
        :pagination="pagination"
      >
        <template slot="action" slot-scope="record">
          <a-button shape="circle" icon="edit" @click="updateInterface(record)" />
          <a-button
            shape="circle"
            icon="delete"
            type="danger"
            style="margin-left: 0.5em"
            @click="
              () => {
                delete_visible = true;
                interface_id = record.id;
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
  getAllModule,
  createInterface,
  updateInterface,
  deleteInterface,
  getInterfaceList
} from "@/api";
import { pagination } from "@/components/base";
export default {
  data() {
    return {
      // 查询表单
      searchForm: {
        name: null,
        uri: null,
        module: undefined,
        flag: undefined,
      },

      // 可选模块
      modules: [],

      // 创建模块弹窗
      visible: false,
      isCreate: true,
      interfaceForm: {
        name: null,
        uri: null,
        module: undefined,
        flag: undefined,
      },

      // 表格
      loading: false,
      interfaceList: [],
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
          width: "10%",
        },
        {
          title: "URI",
          dataIndex: "uri",
          align: "center",
          width: "25%",
        },
        {
          title: "归属模块",
          dataIndex: "module_name",
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
      pagination: pagination(this.queryInterfaces, ["20", "50", "100"]),

      // 删除变量
      delete_visible: false,
      interface_id: null,
    };
  },
  methods: {
    // 弹窗确认回调
    handleOk() {
      this.$refs.interfaceForm.validate((valid) => {
        if (valid) {
          if (this.isCreate) {
            createInterface(this.interfaceForm).then((res) => {
              this.$message.success(res.data.msg);
              this.visible = false;
              this.$refs.interfaceForm.resetFields();
              this.queryInterfaces();
            });
          } else {
            updateInterface(this.interfaceForm).then((res) => {
              this.$message.success(res.data.msg);
              this.visible = false;
              this.interfaceForm = {
                name: null,
                uri: null,
                module: undefined,
                flag: undefined,
              };
              this.queryInterfaces();
            });
          }
        }
      });
    },
    // 弹窗取消回调
    handleCancel() {
      this.visible = false;
      this.$refs.interfaceForm.resetFields();
    },
    // 查询接口列表
    queryInterfaces() {
      this.loading = true;
      this.searchForm.page = this.pagination.current;
      this.searchForm.page_size = this.pagination.pageSize;
      getInterfaceList(this.searchForm).then((res) => {
        this.interfaceList = res.data.data;
        this.pagination.total = res.data.total;
        this.loading = false;
      });
    },
    // 更新接口
    updateInterface(row) {
      this.visible = true;
      this.isCreate = false;
      this.interfaceForm = JSON.parse(JSON.stringify(row));
    },
    // 删除接口
    handleDeleteOk() {
      deleteInterface(this.interface_id).then((res) => {
        this.$message.success(res.data.msg);
        this.queryInterfaces();
      });
      this.delete_visible = false;
    },
  },
  created() {
    getAllModule().then((res) => {
      this.modules = res.data;
    });
    this.queryInterfaces();
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