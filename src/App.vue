<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    
  }),
  created() {
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    if(UserInfo.auto_login == false) {
      console.log("오토 로그인 미선택 - 로그인 화면 이동");
      localStorage.removeItem("UserInfo");
      router.push({name: 'login'});
    }
  }
};
</script>
