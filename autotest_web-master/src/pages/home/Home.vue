<template>
    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <home-header></home-header>
        </el-header>

        <el-container>
            <el-aside style="width: 202px">
                <home-side></home-side>
            </el-aside>

            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>


</template>

<script>
    import HomeHeader from './components/Header'
    import HomeSide from './components/Side'

    export default {
        name: "Home",
        components: {
            HomeHeader,
            HomeSide
        },
		methods:{
			islogin() {
				//获取localStorage中token的值，如果null，进入登录界面
				// console.log("---------token------------1")
				// token = this.getLocalValue("token")
				// console.log("---------token------------2")
				// console.log("---------token------------", token)
				// if (token == "null"){
				// 	this.$router.push({name:"Login"});
				// }
			},
		},
		mounted() {
		    this.islogin()
		},

    }
</script>

<style scoped>
    .el-main {
        padding: 0px;
    }

</style>
