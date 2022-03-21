<template>
  <div>
    <!-- 搜索区域 -->
    <div id="search-scope">
      <!-- 搜索表单 -->
      <a-form-model ref="searchForm" layout="inline" :model="searchForm">
        <a-form-model-item label="服务名称" prop="name">
          <a-input placeholder="精确匹配" v-model="searchForm.name"></a-input>
        </a-form-model-item>
        <a-form-model-item label="协议" prop="protocol">
          <a-select placeholder="请选择" v-model="searchForm.protocol">
            <a-select-option v-for="item in protocols" :value="item[0]" :key="item[0]">{{ item[1] }}</a-select-option>
          </a-select>
        </a-form-model-item>
        <a-form-model-item label="服务域名" prop="domain">
          <a-input placeholder="模糊匹配" v-model="searchForm.domain"></a-input>
        </a-form-model-item>
        <a-form-model-item label="端口号" prop="port">
          <a-input placeholder="精确匹配" v-model="searchForm.port"></a-input>
        </a-form-model-item>
        <a-form-model-item label="是否可用" prop="flag">
          <a-select v-model="searchForm.flag" placeholder="请选择">
            <a-select-option :value="1">是</a-select-option>
            <a-select-option :value="0">否</a-select-option>
          </a-select>
        </a-form-model-item>
      </a-form-model>
      <!-- 操作按钮 -->
      <a-row id="button-scope">
        <a-col :span="12" style="text-align: left">
          <a-button type="primary" @click="() => { visible = true; isCreate = true}">创建服务</a-button>
        </a-col>
        <a-col :span="12" style="text-align: right">
          <a-button type="primary" @click="queryServices()">查询</a-button>
          <a-button @click="$refs.searchForm.resetFields()">重置</a-button>
        </a-col>
      </a-row>
      <!-- 创建服务弹窗 -->
      <a-modal
        id="modal"
        title="创建服务"
        :visible="visible"
        @ok="handleOk"
        @cancel="handleCancel"
        width="30em"
      >
        <a-form-model ref="serviceForm" :model="serviceForm" :wrapperCol="{span: 18, offset: 3}">
          <a-form-model-item prop="name" required>
            <a-input v-model="serviceForm.name" placeholder="服务名称">
              <a-icon slot="prefix" type="cloud" style="color:rgba(0,0,0,.25)" />
            </a-input>
          </a-form-model-item>
          <a-form-model-item prop="domain" required>
            <a-input v-model="serviceForm.domain" placeholder="域名">
              <a-icon slot="prefix" type="fire" style="color:rgba(0,0,0,.25)" />
            </a-input>
          </a-form-model-item>
          <a-form-model-item prop="protocol" required>
            <a-select placeholder="请选择" v-model="serviceForm.protocol">
              <a-select-option
                v-for="item in protocols"
                :value="item[0]"
                :key="item[0]"
              >{{ item[1] }}</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="port">
            <a-input v-model="serviceForm.port" placeholder="端口号">
              <a-icon slot="prefix" type="shrink" style="color:rgba(0,0,0,.25)" />
            </a-input>
          </a-form-model-item>
          <a-form-model-item prop="flag" required>
            <a-select v-model="serviceForm.flag">
              <a-select-option :value="1">是</a-select-option>
              <a-select-option :value="0">否</a-select-option>
            </a-select>
          </a-form-model-item>
        </a-form-model>
      </a-modal>
    </div>
    <!-- 表格区域 -->
    <div id="list-scope">
      <a-table
        :columns="columns"
        :data-source="serviceList"
        :rowKey="record => { return record.id } "
        :pagination="pagination"
      >
        <template slot="action" slot-scope="record">
          <a-button shape="circle" icon="edit" @click="updateService(record)" />
        </template>
        <template slot="flag" slot-scope="text">{{ text == true ? "可用" : "不可用" }}</template>
      </a-table>
    </div>
  </div>
</template>
<script>
import { getProto, createService, updateService, getServiceList } from "@/api";

export default {
  data() {
    return {
      // 查询表单
      searchForm: {
        name: null,
        domain: null,
        protocol: undefined,
        port: null,
        flag: undefined // 下拉框初始值定义为undefined时，placeholder才会展示
      },

      // 可选协议
      protocols: [],

      // 创建任务弹窗
      visible: false,
      isCreate: true,
      serviceForm: {
        name: null,
        domain: null,
        protocol: 0,
        port: null,
        flag: 1
      },

      // 表格
      serviceList: [],
      columns: [
        {
          title: "ID",
          dataIndex: "id",
          align: "center",
          width: "10%"
        },
        {
          title: "名称",
          dataIndex: "name",
          align: "center",
          width: "20%"
        },
        {
          title: "协议",
          dataIndex: "protocol_str",
          align: "center",
          width: "10%"
        },

        {
          title: "域名",
          dataIndex: "domain",
          align: "center",
          width: "30%"
        },
        {
          title: "端口",
          dataIndex: "port",
          align: "center",
          width: "10%"
        },
        {
          title: "状态",
          dataIndex: "flag",
          scopedSlots: { customRender: "flag" },
          align: "center",
          width: "10%"
        },
        {
          title: "操作",
          scopedSlots: { customRender: "action" },
          align: "center"
        }
      ],

      // 分页
      pagination: {
        total: 0,
        current: 1,
        pageSize: 10,
        showTotal: total => `共 ${total} 条数据`,
        showSizeChanger: true,
        showLessItems: true,
        pageSizeOptions: ["10", "20", "50", "100"],
        onShowSizeChange: this.onPage,
        onChange: this.onPage
      }
    };
  },
  methods: {
    // 弹窗确认回调
    handleOk() {
      this.$refs.serviceForm.validate(valid => {
        if (valid) {
          if (this.isCreate) {
            createService(this.serviceForm).then(res => {
              this.$message.success(res.data.msg);
              this.visible = false;
              this.$refs.serviceForm.resetFields();
              this.queryServices();
            });
          } else {
            updateService(this.serviceForm).then(res => {
              this.$message.success(res.data.msg);
              this.visible = false;
              this.serviceForm = {
                name: null,
                domain: null,
                protocol: 0,
                port: null,
                flag: 1
              };
              this.queryServices();
            });
          }
        }
      });
    },
    // 弹窗取消回调
    handleCancel() {
      this.visible = false;
      this.$refs.serviceForm.resetFields();
    },
    // 查询服务列表
    queryServices() {
      this.searchForm.page = this.pagination.current;
      this.searchForm.page_size = this.pagination.pageSize;
      getServiceList(this.searchForm).then(res => {
        this.serviceList = res.data.data;
        this.pagination.total = res.data.total;
      });
    },
    // 更新服务
    updateService(row) {
      this.visible = true;
      this.isCreate = false;
      this.serviceForm = JSON.parse(JSON.stringify(row));
    },
    // 分页回调
    onPage(current, pageSize) {
      this.pagination.current = current;
      this.pagination.pageSize = pageSize;
      this.queryServices();
    }
  },
  mounted() {
    getProto().then(res => {
      this.protocols = res.data;
    });
    this.queryServices();
  }
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