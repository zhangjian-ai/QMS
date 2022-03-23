// 通用分页配置。按需传入对应位置参数
export let pagination = (callback, options = ["10", "20", "50", "100"]) => {
    let config = {
        total: 0,
        current: 1,
        pageSize: Number(options[0]),
        showTotal: total => `共 ${total} 条数据`,
        showSizeChanger: true,
        showLessItems: true,
        pageSizeOptions: options,
        onShowSizeChange: (current, pageSize) => {
            config.current = current;
            config.pageSize = pageSize;
            callback();
        },
        onChange: (current, pageSize) => {
            config.current = current;
            config.pageSize = pageSize;
            callback();
        }
    }

    return config
}