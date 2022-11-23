<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="400" color="#f5efe6" class="pa-3">
          <v-card-title class="my-text recommend-recipe-title pa-5">
            추천 레시피
          </v-card-title>

          <!-- 추천 레시피 v-card -->
          <v-card height="100" class="mx-5 mb-5" v-for="item in 5" color="#E8DFCA">
            <div class="d-flex align-center">
              <!-- 음식을 받아와서 넣으시면 됩니다. -->
              <span class="mx-10 py-3" style="font-size:1.1em; font-weight:600; color:#7895B2">김치볶음밥</span>
              <v-icon color="red" v-if="item%5+1>=1">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="item%5+1>=2">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="item%5+1>=3">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="item%5+1>=4">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="item%5+1>=5">mdi-chili-mild</v-icon>
            </div>
            <div style="border: 0.5px solid #7895B2;" class="mx-5"></div>
            <div class="d-flex align-center justify-space-between">
              <div style="color:#7895B2" class="ml-10 py-3">
                <!-- 날짜를 받아와서 넣으시면 됩니다. -->
                <span class="mr-3">2022/06/07</span>
                <!-- 이름을 받아와서 넣으시면 됩니다 -->
                <span>홍길동</span>
              </div>
              <div class="mr-6">
                <!-- 좋아요 받아와서 넣으시면 됩ㄴ디ㅏ. -->
                <v-icon color="red">mdi-thumb-up-outline</v-icon> 1.1K
                <!-- 댓글 가져와서 넣으시면 됩니다. -->
                <v-icon color="blue" class="ml-2">mdi-comment-processing-outline</v-icon> 5m
                <!-- 조회수 가져와서 넣으시면 됩니다. -->
                <v-icon color="green" class="ml-2">mdi-eye-outline</v-icon> 1.5K
              </div>
            </div>
          </v-card>

        </v-card>

        <v-card min-height="200" color="#f5efe6" class="pa-3 mt-3 overflow-auto">
          <v-card-title class="my-text recommend-recipe-title pa-5">
            추천 요리 사진
          </v-card-title>
          
          <!-- 추천 요리 사진 v-for 입니다. -->
          <div class="d-flex align-center">
            <div v-for="item in 20">
              <v-img
                contain
                max-width="300"
                src="https://picsum.photos/id/11/500/300"
                class="mx-4"
              ></v-img>
            </div>
          </div>
          

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.my-text{
  color: #42688e;
}

.recommend-recipe-title{
  color: #7ca5c9;
  font-weight: 900;
}
</style>

<script>

</script>