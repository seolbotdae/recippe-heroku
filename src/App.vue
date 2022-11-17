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
      localStorage.removeItem("UserInfo");
      router.push({name: 'login'});
    }
  }
};
</script>
