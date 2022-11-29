<template>
  <v-card class="overflow-y-auto">

    <v-card-title class="justify-start">
      카테고리 선택
    </v-card-title>

    <v-card v-for="item in recippeType" :key="item.name" @click="clickCategory(item.name)">
      <v-card-title>{{item.name}}</v-card-title> 
    </v-card>
    
  </v-card>
</template>

<script>
export default{
  name: "Category",
  data() {
    return {
      recippeType: [
        { name: '족발보쌈'},
        { name: '찜탕찌개'},
        { name: '돈까스'},
        { name: '회'},
        { name: '일식'},
        { name: '피자'},
        { name: '고기구이'},
        { name: '야식'},
        { name: '양식'},
        { name: '치킨'},
        { name: '중식'},
        { name: '아시안'},
        { name: '백반'},
        { name: '죽'},
        { name: '국수'},
        { name: '도시락'},
        { name: '분식'},
        { name: '카페디저트'},
        { name: '패스트푸드'},
      ],
    }
  },
  methods: {
    clickCategory(name) {
      this.$emit('category', name);
      this.$emit('hide');
    }
  }
}
</script>