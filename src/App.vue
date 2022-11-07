<template>
  <div>
    <div>app.vue</div>
    <v-btn><router-link to="/create">create</router-link></v-btn>
    <v-btn><router-link to="/table">table</router-link></v-btn>
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>
