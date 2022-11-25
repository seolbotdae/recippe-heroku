<template>
  <v-card>
    <!-- 재료 입력 부분 -->
    <v-card-text>
      <div class="line mx-5" />

      <span>재료 추가</span>
      <div class="line mx-5" />

      <span>개수</span>
      <div class="line mx-5" />

      <span>단위</span>
      <div class="line mx-5" />

      <span>유통기한</span>
      <div class="line mx-5" />
    </v-card-text>

    <!-- 버튼 부분 -->
    <v-card-actions class="justify-center mr-2 pb-4">
      <v-btn
        color="#7895B2"
        small
        @click="addIngre"
      >
        추가하기
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default{
  name: "addIngredient",
  data() {
    return {
      name: "",
      amount: "",
      unit: "",
      expiry_date: "",
      nickname: "",
    };
  },
  mounted(){
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    this.nickname = UserInfo.nickname;
  },
  methods: {
    addIngre() {
      const addIngre = {
        "amount": this.amount,
        "expiry_date": this.expiry_date, // 없어도 됨
        "name" : this.name,
        "nickname" : this.nickname,
        "unit" : this.unit
      };
      this.$emit('add', addIngre);
      this.$emit('hide');
    }
  }
}
</script>