<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <!-- 가장 바깥쪽 카드 -->
        <v-card min-height="1000" color="#f5efe6">
          <!-- 뒤로 돌아가기 버튼 -->
          <v-btn text to="/photo" class="ml-5 mt-5"> - 레시피 게시판</v-btn>
          <!-- 게시글 정보 입력란 -->
          <div class="mt-5">
            <div class="line mx-5"></div>

            <!-- value 를 변수로 채워주시면 됩니다. -->
            <div class="px-10 d-flex align-center">
              <span class="my-text mr-16">레시피 제목</span>
              <v-divider vertical></v-divider>
              <v-text-field
                name="name"
                label="레시피 제목"
                id="id"
                class="ml-16"
                value="고등어 순살 조림"
              ></v-text-field>
            </div>
            
            <div class="line mx-5"></div>

            <!-- script에 recippeTypeObject 를 바꾸시면 됩니다. -->
            <div class="px-10 d-flex align-center">
              <span class="mr-16 my-text">레시피 종류</span>
              <v-divider vertical></v-divider>
              <dropdown class="my-dropdown-toggle ml-15"
              :options="recippeType" 
              :selected="recippeTypeObject" 
              v-on:updateOption="methodToRunOnSelect" 
              :placeholder="'레시피 종류'"
              :closeOnOutsideClick="boolean">
              </dropdown>
            </div>

            <div class="line mx-5"></div>

            <!-- script에 recippeTypeObject 를 바꾸시면 됩니다. -->
            <div class="px-10 d-flex align-center">
              <span class="mr-16 my-text">매운맛 단계</span>
              <v-divider vertical></v-divider>
              <dropdown class="my-dropdown-toggle ml-14"
              :options="hotLevel" 
              :selected="hotLevelObject" 
              v-on:updateOption="methodToRunOnSelect" 
              :placeholder="'매운맛 단계'"
              :closeOnOutsideClick="boolean">
              </dropdown>
            </div>

            <div class="line mx-5"></div>

            <div class="px-10 d-flex wrap align-center ingredients" style="position:relative">
              <span class="ml-1 mr-14 my-text">식재료 및 양</span>
              <v-divider vertical class="mr-11"></v-divider>
              <div class=ma-3>
                <!-- 재료 나타날 v-for -->
                <!-- 재료를 바꾸시면 됩니다. -->
			          <span v-for="item in 30">
			          	<span style="vertical-align: text-top" class="my-text">고등어 1마리</span>
                  <v-btn small text color="success pa-5">
                    <v-icon >mdi-close-box</v-icon>
                  </v-btn>
                  <br/>
                  
			          </span>
              </div>
              
			        
              <div class="d-flex">
                <v-btn color="success pa-5" class="add-ingredient">
                  <v-icon>mdi-plus-circle-outline</v-icon>
                  <span>재료 추가하기</span>
                </v-btn>
              </div>
              
            </div>
            
            <div class="line mx-5"></div>
          </div>

          <!-- 레시피 설명 입력란 -->
          <!-- 여기 value를 바꾸시면 됩니다. -->
          <v-textarea
            outlined
            class="mt-5 mx-5"
            name="name"
            label="레시피 설명을 입력하세요"
            placeholder="레시피 설명을 입력하세요"
			      value="고등어 손질하고 재료 다 넣어서 졸이면 됩니다. ^^"
            height="300"
            background-color="white"
          ></v-textarea>

          <div class="d-flex justify-end mr-5 pb-5">
            <v-btn color="#AEBDCA" class="mr-5">등록취소</v-btn>
            <v-btn color="#AEBDCA" class="mr-2">등록하기</v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
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

export default {
  data () {
	return {
      recippeType: [
        { name: '최근 순'},
        { name: '조회 순'},
        { name: '좋아요 순'}
      ],
      recippeTypeObject: {
        name: '한식',
      },
      hotLevel: [
        { name: '1단계'},
        { name: '2단계'},
        { name: '3단계'},
        { name: '4단계'},
        { name: '5단계'}
      ],
      hotLevelObject: {
        name: '3단계',
      },
    }
  },
  components: {
    'dropdown': dropdown,
  },
  methods: {
    editRecipe() {
      const recipe = JSON.stringify (
        {
	        "post_id": 52,
	        "nickname": "test",
	        "title": "heroku_test2",
	        "category": "heroku_test2",
	        "degree_of_spicy": 5,
	        "description": "heroku_test2",
	        "views": 0,
	        "like_count": 0,
	        "comment_count": 0,
	        "upload_time": "2022-11-21T15:10:03.102840+09:00",
	        "Recipe_Ingredients": [
		        {
			        "id": 54,
			        "name": "yangpa",
			        "post_id": 53,
			        "unit": "T",
			        "amount": 100.0
		        },
		        {
			        "id": 55,
			        "name": "asparagus",
			        "post_id": 53,
			        "unit": "Kg",
			        "amount": 200.0
		        }
	        ],
	        "comments": [
	        ]
        }
      );
      herokuAPI.recipeEdit(recipe) 
        .then(function (response) {
          console.log("전송 정보",  recipe);
          if(response.status == 200) {
            console.log("응답 정보", response.data);
          }
        })
    }
  }
}
</script>