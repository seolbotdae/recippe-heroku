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
              <v-btn @click="showCategoryDialog" class="ml-14">카테고리 선택하기</v-btn>
              <span class="ml-16">카테고리 : {{category}}</span>
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

    <!-- 카테고리 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="categoryDialog"
    >
      <category-dialog
        @category="selectCategory"
        @hide="hideCategoryDialog"
      />
    </v-dialog>

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

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        headerTitle="등록하기 요청 실패"
        btn1Title="확인"
        :btn2="false"
        @hide="hideDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>등록 요청에 실패했습니다.</div>
        </template>
      </popup-dialog>
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
.temp {
  max-height: 100px;
  overflow: scroll;
}

</style>

<script>
import herokuAPI from '@/api/heroku.js';
import dropdown from 'vue-dropdowns';
import router from '@/router/index.js';
import AddIngredientDialog from '@/components/addIngredient.vue';
import PopupDialog from '@/components/popup.vue';
import CategoryDialog from '@/components/Category.vue'

export default{
  components: {
    'dropdown': dropdown,
    PopupDialog,
    AddIngredientDialog,
    CategoryDialog
  },
  data () {
    return {
      addIngredientDialog: false,
      popupDialog: false,
      categoryDialog: false,

      ingredient: [],
      category: "",
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
  // 팝업창 관련
    showDialog() { // 팝업창 보이기
      this.popupDialog = true;
    },
    hideDialog() { // 팝업창 숨기기
      this.popupDialog = false;
    },
    showCategoryDialog() {
      this.categoryDialog = true;
    },
    hideCategoryDialog() {
      this.categoryDialog = false;
    },
    selectCategory(name, page) {
      this.category = name;
    },
  // 재료추가 팝업창 메소드들
    showAddIngredientDialog() {
      this.addIngredientDialog = true;
    },
    hideAddIngredientDialog() {
      this.addIngredientDialog = false;
    },
    add(ingre) {
      const addIngre = {
        "id": null,
        "name": ingre.name,
        "post_id": null,
        "unit": ingre.unit,
        "amount": ingre.amount
      }
      this.ingredient.push(addIngre);
    },
    update() {
      this.$router.go();
    },

    addRecipe() {
      const validate = this.$refs.form.validate();
      if(!validate) return;
      let vm = this;
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      const recipe = JSON.stringify ({
        "post_id": null,
        "nickname": UserInfo.nickname,
        "title": vm.recipeTitle,
        "category": vm.category,
        "degree_of_spicy": vm.recipeSpicy,
        "description": vm.recipeDescription,
        "views": 0,
        "like_count": 0,
        "comment_count": 0,
        "upload_time": null,
        "Recipe_Ingredients": vm.ingredient,
        "comments": []
        });
      console.log("연결 정보", recipe);
      herokuAPI.recipeAdd(recipe) 
        .then(function (response) {
          console.log("전송 정보",  recipe);
          if(response.status == 200) {
            console.log("응답 정보", response);
            console.log("응답 정보", response.data);
            router.push({path: "/recipe"});
          }
        })
        .catch(function (e) {
          if(e.response.status == 500) {
            console.log("500 DB error");
            vm.showDialog();
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
            vm.showDialog();
          }
        });
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