<template>
  <v-container>
    비밀번호 수정 화면
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      email: null,
    }
  },
  mounted() {
    this.email = localStorage.getItem("email");
    console.log(this.email);
    localStorage.removeItem("email");
  }
}
</script>