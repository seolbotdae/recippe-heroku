<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
  beforeDestroy() {
    const User = JSON.parse(localStorage.getItem("UserInfo"));
    if(User.auto_login == false) {
      localStorage.removeItem("UserInfo");
    }
  }
};
</script>
