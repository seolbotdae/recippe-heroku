<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <!-- 가장 바깥쪽 카드 -->
        <v-card min-height="1000" color="#f5efe6">
          <!-- 뒤로 돌아가기 버튼 -->
          <v-btn text to="/recipe" class="ml-5 mt-5"> - 레시피 게시판</v-btn>
          <!-- 게시글 정보 입력란 -->
          <v-form ref="form" lazy-validation class="mt-5">
            <div class="line mx-5"></div>

            <div class="px-10 d-flex align-center my-text">
              <span class="mr-16">레시피 제목</span>
              <v-divider vertical />
              <v-text-field
                name="name"
                label="레시피 제목"
                id="id"
                class="ml-16"
                v-model="recipeTitle"
                :rules="title_rule"
              ></v-text-field>
            </div>
            
            <div class="line mx-5"></div>

            <div class="px-10 d-flex align-center my-text">
              <span class="mr-16">레시피 종류</span>
              <v-divider vertical></v-divider>
              <dropdown class="my-dropdown-toggle ml-15"
                :options="recippeType" 
                :selected="recippeTypeObject" 
                v-on:updateOption="methodToRunOnSelect_category" 
                :placeholder="'레시피 종류'"
                :closeOnOutsideClick="true"
              />
            </div>

            <div class="line mx-5"></div>

            <div class="px-10 d-flex align-center my-text">
              <span class="mr-16">매운맛 단계</span>
              <v-divider vertical></v-divider>
              <dropdown class="my-dropdown-toggle ml-15"
                :options="hotLevel" 
                :selected="hotLevelObject" 
                v-on:updateOption="methodToRunOnSelect_spicy" 
                :placeholder="'매운맛 단계'"
                :closeOnOutsideClick="true"
              />
            </div>

            <div class="line mx-5"></div>

            <div class="px-10 d-flex wrap align-center ingredients" style="position:relative">
              <span class="ml-1 mr-14 my-text">식재료 및 양</span>
              <v-divider vertical class="mr-11" />
              <div class=ma-3>
                <!-- 재료 나타날 v-for -->
			          <div v-for="(item,index) in ingredient" :key="item.name">
			          	<span style="vertical-align: text-top" class="my-text">{{ item.name }} {{ item.amount }}{{ item.unit }}</span>
                  <v-btn @click="ingredient.splice(index,1)" small text color="success pa-5">
                    <v-icon>mdi-close-box</v-icon>
                  </v-btn>
                  <br/>
                  
			          </div>
              </div>
              
			        
              <div class="d-flex">
                <v-btn @click="showAddIngredientDialog" color="success pa-5" class="add-ingredient">
                  <v-icon>mdi-plus-circle-outline</v-icon>
                  <span>재료 추가하기</span>
                </v-btn>
              </div>
              
            </div>
            
            <div class="line mx-5"></div>
          </v-form>

          <!-- 레시피 설명 입력란 -->
          <v-textarea
            outlined
            class="mt-5 mx-5"
            name="name"
            label="레시피 설명을 입력하세요"
            placeholder="레시피 설명을 입력하세요"
            height="300"
            background-color="white"
            v-model="recipeDescription"
            :rules="description_rule"
          ></v-textarea>

          <div class="d-flex justify-end mr-5 pb-5">
            <v-btn color="#AEBDCA" class="mr-5">등록취소</v-btn>
            <v-btn color="#AEBDCA" class="mr-2" @click="addRecipe()">등록하기</v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- 재료 추가 팝업창 -->
    <v-dialog
      max-width="500"
      v-model="addIngredientDialog"
    >
      <add-ingredient-dialog
        :isRecipe='true'
        @add="add"
        @update="update"
        @hide="hideAddIngredientDialog"
      />
    </v-dialog>

  </v-container>
</template>

<style scoped>
.line{
  border:1px solid #AEBDCA
}

.ingredients{
  min-height: 300px;
}

.add-ingredient{
  position: absolute;
  bottom: 5%;
  right: 5%;
}

.my-text{
  color: #42688e;
}

</style>

<script>
import herokuAPI from '@/api/heroku.js';
import dropdown from 'vue-dropdowns';
import AddIngredientDialog from '@/components/addIngredient.vue';

export default{
  components: {
    'dropdown': dropdown,
    AddIngredientDialog
  },
  data () {
    return {
      addIngredientDialog: false,
      ingredient: [],
      recippeType: [
        { name: '최근 순'},
        { name: '조회 순'},
        { name: '좋아요 순'}
      ],
      recippeTypeObject: {
        name: '레시피 종류',
      },
      hotLevel: [
        { name: '1단계'},
        { name: '2단계'},
        { name: '3단계'},
        { name: '4단계'},
        { name: '5단계'}
      ],
      hotLevelObject: {
        name: '매운맛 단계',
      },
      recipeTitle: null,
      title_rule: [
        v => !!v || '제목을 입력하세요.',
      ],
      recipeCategory: null,
      recipeSpicy: 0,
      recipeDescription: null,
      description_rule: [
        v => !!v || '내용을 입력하세요.',
      ],
    }
    
  },
  methods: {
  // 재료추가 팝업창 메소드들
    showAddIngredientDialog() {
      this.addIngredientDialog = true;
    },
    hideAddIngredientDialog() {
      this.addIngredientDialog = false;
    },
    add(ingre) {
      this.ingredient.push(ingre);
    },
    update() {
      this.$router.go();
    },

    addRecipe() {
      let vm = this;
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      const recipe = JSON.stringify ({
        "post_id": 0,
        "nickname": UserInfo.nickname,
        "title": vm.recipeTitle,
        "category": vm.recipeCategory,
        "degree_of_spicy": vm.recipeSpicy,
        "description": vm.recipeDescription,
        "views": 0,
        "like_count": 0,
        "comment_count": 0,
        "upload_time": "",
        "Recipe_Ingredients": vm.ingredient,
        "comments": []
        });
      console.log("연결 정보", recipe);
      /* 데이터 연결한거 테스트를 위해 콘솔에 출력만 시킬라고 요거 주석처리해뒀어 나중에 적용시킬 때 풀면됨 && 등록하기 버튼에 붙어있음 - 요하
      herokuAPI.recipeAdd(recipe) 
        .then(function (response) {
          console.log("전송 정보",  recipe);
          if(response.status == 200) {
            console.log("응답 정보", response.data);
          }
        })
      */
    },
    methodToRunOnSelect_category(payload) {
      this.object = payload;
      this.recipeCategory = this.object.name
    },
    methodToRunOnSelect_spicy(payload) {
      this.object = payload;
      if(this.object.name == "0단계") this.recipeSpicy = 0;
      else if(this.object.name == "1단계") this.recipeSpicy = 1;
      else if(this.object.name == "2단계") this.recipeSpicy = 2;
      else if(this.object.name == "3단계") this.recipeSpicy = 3;
      else if(this.object.name == "4단계") this.recipeSpicy = 4;
      else if(this.object.name == "5단계") this.recipeSpicy = 5;
    }
  }
}
</script>