<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script>
import router from '@/router/index.js';

export default {
  name: 'App',

  data: () => ({
    
  }),
  created() {
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    if(UserInfo == null) {
      router.push({name: 'login'});
    } else if(UserInfo.auto_login == false) {
      localStorage.removeItem("UserInfo");
      router.push({name: 'login'});
    }
  }
};
</script>
