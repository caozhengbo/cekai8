<template>
    <div>
        <div>
            <div>
                <el-input
                    style="width: 600px"
                    placeholder="请输入用例名称"
                    v-model="name"
                    clearable
                >
                    <template slot="prepend">用例信息录入</template>

                    <el-button
                        slot="append"
                        type="success"
                        plain
                        @click="save = !save"
                    >保存
                    </el-button>

                </el-input>

                <el-button
                    slot="append"
                    type="danger"
                    @click="esc = !esc"
                >返回
                </el-button>

               <!-- <el-button
                    type="primary"
                    @click="handleRun"
                    v-loading="loading"
                >Run
                </el-button>-->

            </div>
            <div>

             <el-input
                    style="width: 600px; margin-top: 10px"
                    placeholder="请输入用例描述"
                    v-model="describe"
                    clearable
                >
                <template slot="prepend">用例描述</template>

                </el-input>
            </div>
            <el-dialog
                v-if="dialogTableVisible"
                :visible.sync="dialogTableVisible"
                width="70%"
            >
                <report :summary="summary"></report>
            </el-dialog>
        </div>

        <div class="request">
            <el-tabs
                style="margin-left: 20px"
                v-model="activeTag"
            >
                <el-tab-pane label="用例步骤" name="first">
                    <testcase
                        :save="save"
                        v-on:testcase="handleHeader"
                        :testcase="testcase">
                    </testcase>
                </el-tab-pane>

            </el-tabs>
        </div>
    </div>

</template>

<script>
    
    import Testcase from '../../../uitestpage/uitestcaseplan/components/Testcases'
    import Report from '../../../reports/DebugReport'

    export default {
        components: {
            Testcase,          
            Report

        },

        props: {
            response: {
                require: true
            },
        
        },
        methods: {
          /*  handleRun() {
                this.run = true;
                this.save = !this.save;
            },
*/
            handleHeader(testcase, value) {
                this.testcase = value;

        
                this.tempBody.describe = this.describe;
                this.tempBody.body=testcase
                this.tempBody.name = this.name;
                

                if (this.validateData()) {
                    const body = {
                        body: this.testcase,
                        describe: this.describe,                       
                        name: this.name,                       
                    };
                    this.$emit('getNewBody', body, this.tempBody);
                    this.run = false;
                    
                }
            },
            // handleHeader(testcase){
            //     this.testcase=testcase
            // },

            validateData() {
                if (this.describe === '') {
                    this.$notify.error({
                        title: '用例描述错误',
                        message: '用例描述不能为空',
                        duration: 1500
                    });
                    return false;
                }

                if (this.name === '') {
                    this.$notify.error({
                        title: 'name错误',
                        message: '用例名称不能为空',
                        duration: 1500
                    });
                    return false;
                }
                return true
            }
        },

        watch: {
            esc() {
                this.$emit('escEdit');
            }
        },
        data() {
            return {
                loading: false,
                run: false,
                esc: false,                
                name: this.response.name,
                describe: this.response.describe,
                testcase: [],              
                tempBody: {},            
                save: false,
                summary: {},
                dialogTableVisible: false,
                activeTag: 'first',
                
            }
        },
        name: "TestBody",
        mounted() {
            this.testcase = this.response.body;
       
        }
    }
</script>

<style scoped>
    .el-select {
        width: 125px;
    }

    .input-with-select {
        width: 600px;
        margin-top: 10px;
    }

    .request {
        margin-top: 15px;
        border: 1px solid #ddd;
    }

</style>
