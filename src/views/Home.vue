<template>
  <v-container>
    <v-row>
      <v-col>
        <div>app.vue</div>
      </v-col>
    </v-row>
    <v-row>
      <v-col>home 화면</v-col>
    </v-row>
  </v-container>
</template>

<script>
import router from '@/router/index.js';

export default {

  created() {
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    if(UserInfo.auto_login == false) {
      localStorage.removeItem("UserInfo");
      router.push({name: 'login'});
    }
    if(UserInfo == null) {
      router.push({name: 'login'});
    }
  }
}
</script>