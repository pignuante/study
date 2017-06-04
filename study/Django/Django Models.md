

## 1. Model Syntax

>  model은 소위 말하는 DB의 하나의 table 의미하며 하위의 특징들을 가지고 있다.
>
> - 각각의 모델은 파이썬 class로 표현. `django.db.models.Model` 클래스의 서브 클래스
>
>
> - 모델 클래스의 변수로 DB의 필드(column)을 표현한다.
>
>
> - 이러한 모델 클래스를 통해서 DB 접근  API를 제공한다.

<br><br>

1. #### **Quick Example**

   ```python
   from django.db import models

   class Person(models.Model):
       first_name = models.CharField(max_length=30)
       last_name = models.CharField(max_length=30
   ```

   위 명령어를 django에서 

   ```sql
   CREATE TABLE myapp_person (
       "id" serial NOT NULL PRIMARY KEY,
       "first_name" varchar(30) NOT NULL,
       "last_name" varchar(30) NOT NULL
   );
   ```

   라는 sql query문으로 변경해준다.
   <br><br>

2. #### Fields**

   모델에서 가장 중요한 것은 Field의 선언인데 필드는 클래스의 어트리뷰트로 표현되어집니다.

   ```python
   class Musician(models.Model):
       first_name = models.CharField(max_length=50)
       last_name = models.CharField(max_length=50)
       instrument = models.CharField(max_length=100)
   class Album(models.Model):
       artist = models.ForeignKey(Musician) # musician을 가지는
       name = models.CharField(max_length=100)
       release_date = models.DateField()
       num_start = models.IntegerField()
   ```

   1. Field types

      django는 각 필드의 클래스 타입을 통하여 아래와 같은 내용을 자동적으로 판단하여 작동해줍니다.

      - DB 칼럼 타입 e.x) INTEGER, VARCHAR
      - Django Form을 이용하여 모델을 HTML로 랜더링 할떄 어떤 식으로 표현 할지
        e.x) `<input type="text"><select>`
      - Django Admin 페이지나 자동생성된 form에서 수행될 최소한의 유효성 체크(vValidation)

      다양한 내장된 필드 타입을 제공하며, 직접 우리가 만들어 사용할수도 있다.

      ​

      ​
      <br>

   2. Field options

      각 필드에는 다양한 옵션을 줄수있다.

      |   option    |        description         |
      | :---------: | :------------------------: |
      |    null     |     해당 컬럼에 NULL값 부여 가능     |
      |    blank    |    값을 입력하지 않아도 된다.[^1]     |
      |   choices   |  필드 값의 종류를 제한하고 싶을때.[^2]   |
      |   default   |     해당 필드의 기본 값을 정의한다.     |
      |  help_text  |   해당 필드가 표시될 때 표시될 도움말.    |
      | primary_key |    pk, 해당 필드의 고유값.[^3]     |
      |   unique    | 해 당 테이블에서 중복되는 값을 가지지 못한다. |

      <br>

   3. Automatic Primary Key Fields

      ```python
      id = models.AutoField(primary_key=True)
      ```

      기본적으로 model들은 위와 같은 필드를 자동으로 가지게 된다.

      만약 직접 primary_key를 설정하고 싶으면 우리가 만든 모델의 필드중 하나에 `primary_key=True`를 주면 된다.

      <br>

   4. Verbose field names

      내가 만든 필드의 이름을 표기 해줄수 있다.

      ```python
      first_name = models.CharField("person's first name", max_length=30)
      poll = models.ForeignKey(Poll, verbose_name="the related poll")
      sites = models.ManyToManyField(Site, verbose_name="list of sites")
      place = models.OneToOneField(Place, verbose_name="related place")
      ```

      라고 하면 fisrt_name을 사용할 때 "person's first name"라고 사용 할 수 있다.

      <br>

   5. **Relationships**

      관계형 데이터베이스를 제공해준다!!!!(으아아아악) 이 관계에 있어서 무결성을 보장해준다.

      Django는 3가지 대표적인 데이터베이스 관계형태(일대다, 다대다, 일대일)을 제공한다.

      1. Many-to-One relationships

         일대다 관계를 정의하려면 `django.db.models.ForeignKey`클래스를 이용하여 필드를 선언한다.

         ```python
         class Manufacturer(models.Model):
             pass
         class Car(models.Model):
             manufacturer = models.ForeignKey(Manufacturer)
             
         ```

         <br>

      2. Many-to-Many relationships

         다대다의 관계를 선언할때에는 `ManyToManyField()`를 사용합니다. 첫 번째 인자로 관계를 가지는 클래스를 받습니다.

         ```python
         from django.db import models

         class Topping(models.Model):
             pass
         class Pizza(models.Model):
             toppings = models.ManyToManyField(Topping)
         ```

         토핑은 피자 하나에 여러가지가 들어갈수있으므로 many to many로 선언하였다. 이 관계는 두 필드 중 어느것에 선언해도 상관없으나 사용자의 편의에 편 한곳으로 하는 것이 좋다.

      3. Extra fields on Many-to-Many relationships

         다대다 관계에서 추가로 파생되는 데이터를 저장할 모델이 필요할떄가 있다.

         이를 **intermediate**모델이라고 한다.

         ```python
         from django.db import models

         class Person(models.Model):
             pass
         class Group(models.Model):
             ...
             members = models.ManyToManyField(Person, thought="Membership")
             pass
         class Membership(models.Model):
             pass
         ```

         <br>

      4. One-to-One relationships

         일대일 관계를 정의라하려면 OneToOneField를 사용하면 된다.
         <br><br>

   6. **Models Across files**
      다른 앱에 선언되어 있는 모델과 관계를 가질 수 있습니다. 다른 모델을 사용하기 위해서 import한 다음 설정해주면 됩니다.

      ```python
      from django.db import models
      from geography.models import ZipCode

      class Restaurant(models.Model):
          zip_code = models.ForeignKey(ZipCode)
      ```

      <br><br>

   7. **Field name restrictions**

      django모델 필드 이름에는 2가지 제약이 있다.

      1. 파이썬 **예약어**는 사용이 불가능하다
      2. 필드이름에는 밑줄 두개*(dunder)*를 사용할수 없다.

      <br><br>

   8. Custom field types

      django에서 제공하는 데이터 type중 내가 원하는 것이 없으면 필드를 직접 제작하여 사용할수도 있다. 이 부분은 [django 공식문서](https://www.djangoproject.com/download/)를 참고하자.

      <br><br><br>

3. #### Meta options

   ```python
   from django.db import models

   class OX(models.Model):
       horn_length = models.IntegerField()
       
       class Meta:
           ordering = ["horn_length"]
           verbose_name_plural = "oxen"
           
   ```

   모델 클래스 내부에 `Meta`라는 이름의 클래스를 선언해서 모델에서 메타 데이터를 이용할수 있다. 

   *모델 메타데이터*는 앞에 서보았던 필드단위의 옵션들과 달리 <u>모델 단위</u>의 옵션이다.

   모든 메타 데이터 옵션들을 살펴보려면 [model option reference](https://docs.djangoproject.com/en/1.11/ref/models/options/)를 참조하자.

   <br><br>

4. #### Model Attributes

   1. 아직 이해가 잘 안간다.

5. #### Model Methods

   한 테이블 내에서 row단위의 기능을 구현하려면 모델 class안에 method를 구현하면된다. table단위의 기능을 구현하려면 manager에서 구현한다.

   ```python
   from django.db import models

   class Person(models.Model):
       first_name = models.CharField(max_length=50)
       last_name = models.CharField(max_length=50)
       birth_date = models.DateField()
       
       def baby_boomer_status(self):
           "Returns the person's baby-boomer status."
           import datetime
           if self.birth_date < datetime.date(1945, 8, 1):
               return "Pre-boomer"
           elif self.birth_date < datetime.date(1965, 1, 1):
               return "Baby boomer"
           else:
               return "Post-boomer"
       def _get_full_name(self):
           "Returns the person's full name."
           return "{} {}".format(self.name, self.last_name)
       
       full_name = property(_get_full_name)
   ```

   [model instance reference](https://docs.djangoproject.com/en/1.11/ref/models/instances/)를 보면 클래스에 자동적으로 주어지는 method를 볼수있다. 

   - `__unicode__()`(Python 2), `__str__()`(python3)

     모델 객체가 문자열로 표현되어야 할 경우에 호출.

   - `get_absolute_url()`

     django가 해당 모델 객체의 URL을 계산할 수 있도록 합니다. 모델 객체가 유일한 URL을 가지는 경우 이 메서드를 구현해주어야 합니다.

   - Overrinding predefined model methods

     모델 class가 제공하는 기본적인 method들을 커스터마이즈 하고자 하는 경우가 있는데(특히나 delete() save()등), 이렇나 메소드들도 얼마든지 오버라이드해서 동작을 수정할 수 있습니다.

     ```python
     from django.db import models

     class Blog(models.Model):
         name = models.CharField(max_length=100)
         tagline = models.TextField()
         
         def save(self, *args, **kwargs):
             do_something()
             super(Blog, self).save(*args, **kwargs) 
             do_something_else()
     ```

     뿐만 아니라 SQL문을 직접 작성하여 사용도 가능하다.

     <br><br>

6. #### Model inheritance

   django에서의 상속은 python에서의 상속처럼 이루어져진다. 단 model상속의 경우 base class는 django.db.models.Model 클래스의 서브 클래스여야 한다. 

   django는 3가지의 상속 모델이 존재한다.

   1. Abstract 

      부모 클래스는 추상으로 테이블의 개념만 만들어두고 자식 클래스이서 구체화 시키는 상속.

   2. Multi-table 

      이미 존재(사용되는 모델)의 상속을 받는다. 부모 모델은 자신의 DB table을 가지며 자식 모델과는 별개로 사용가능하다.

   3. Proxy

      모델의 필드 선언은 전혀 변경하지 않고 파이썬 레벨의 코드만 수정하고자 하는 경우 사용하는 방법이다.

   - Abctract Base Class 

     ```python
     from django.db import models

     class CommonInfo(models.Model):
         name = models.CharField(max_length=100)
         age = models.PositiveIntegerField()

         class Meta:
             abstract = True

     class Student(CommonInfo):
         home_group = models.CharField(max_length=5)
         
     ```

     Student는 comminInfo의 정보를 가지는 테이블이다. 부모 클래스의 정보를 가지면서 추가로 `home_group`라는 필드를 가진다.

     (???? student를 여러개 만들면 Commoninfo는 몇개가 생성될까?)

   - Meta Inheritance
     자식 class가 Meta 클래스를 가지지 않을 경우, 부모의 meta class를 상속 받는다. 만약 부모의 meta 클래스를 상속 extend하려면 아래와 같이 부모 클래스에 선언된 Meta 클래스로 부터 상속 받으면 된다.

     ```python
     from django.db import models

     class CommonInfo(models.Model):
         # ...
         class Meta:
             abstract = True
             ordering = ['name']

     class Student(CommonInfo):
         # ...
         class Meta(CommonInfo.Meta):
             db_table = 'student_info'
     ```

     이 경우 `CommonInfo`클래스는 abstract 클래스인데 자식이 상속 받을 때에 `abstract` 옵션을 자동으로 False로 변경한다. 또한 몇몇 Meta 클래스 옵션은 추상클래스에서는 사용이 불가하다.(주의)

   - foreign key로 여러 테이블을 참조 할 경우 `related_name`의 사용을 주의해야한다. 하나의 테이블에 여러 테이블이 하나의 `related_name`을 참조 할 경우 여러가지 문제가 발생한다. 이럴 때에는 `related_name`에 `app`의 이름과 `class`의 이름을 조합하여 사용하면 어느정도 해결이 가능하다.

     ```python
     # common/models.py

     from django.db import models

     class Base(models.Model):
         m2m = models.ManyToManyField(OtherModel, related_name="%(app_label)s_%(class)s_related")

         class Meta:
             abstract = True

     class ChildA(Base):
         pass

     class ChildB(Base):
         pass
     ```

     ```python
     # rare/models.py:

     from common.models import Base

     class ChildB(Base):
         pass
     ```

     common/models.py에 선언된 클래스들 부터 살펴봅시다. ChildA.m2m 필드의 역참조 이름은 common_childa_related 가 되며, ChildB.m2m 필드는 common_childb_related 가 됩니다. 즉, OtherModel은 common_childa_related, common_childb_related 두 개의 역참조 어트리뷰트를 가지게 됩니다.

     rare/models.py 에 선언된 모델의 경우에 역참조 이름은 rare_childb_related 가 됩니다. 

     참고로, 만약 이 경우에 Base 모델 클래스에서 m2m 필드에 related_name 옵션을 지정하지 않으면, 상속받은 자식클래스의 이름을 기준으로 역참조 이름이 결정됩니다. 즉, ChildA 클래스는 childa_set, ChildB 클래스는 childb_set 으로 역참조 이름이 결정됩니다. 

     그런데, 위의 예제에서 common 앱과 rare 앱이 동일한 이름의 모델(ChildB)이 Base 모델을 상속받았습니다. 그러므로 역참조 이름이 중복(childb_set)되어 에러가 발생됩니다.

   - Multi-table inheritance

     Multi-table inheritance은 부모건 모델이간 모두 각자의 DB table을 가진다. 공통부분은 모두 부모에 들어 있고 자식모델만의 데이터는 자식에 저장되며, 자식은 부모에 대한 링크를 가진다. 이때 링크는 내부적으로 **OneToOneField**를 가진다.

     ```python
     from django.db import models

     class Place(models.Model):
     	name = models.CharField(max_length=50)
         address = models.CharField(max_length=80)

     class Restaurant(Place):
         serves_hot_dogs = models.BooleanField(default=False)
         serves_pizza = models.BooleanField(default=False)    
     ```

     Place 모델에 선언된 모든 필드는 Restaurant 모델에서도 사용이 가능하고 각 모델의 필드 값들은 서로 다른 테이블에 각각 저장된다.

   - Meta and multi table inheritance
     multi table 상속 관계에서 자식 모델은 부모의 meta class를 상속 받아야 할까? 부모 와 자식이 모두 자신의 table을 가지기 때문에 meta class를 상속 받는 경우엔 여러가지 문제를 발생시킬수 있다.

     <br><br><br>

7. Procy models

   multi-table 상속을 사용하는 경우 각각의 자식 클래스마다 table이 생성된다. 하지만 가끔 부모 model의 method만 재정의 한다던가 새로 추가하고 싶은 경우엔 모델은 삭속받되, 자식모델은 테이블을 만들 필요가 없는 경우다. 

   이럴 경우엔 **Proxy 모델 상속**을 이용한다. proxy모델(자식 모델)을 이용하여 모델 객체를 만들고, 수정하고 삭제 할 수도 있다. 이러한 동작은 원본(부모)모델 테이블 상에서 이뤄진다.

   Proxy 모델이 원본 모델과 다른 점은 기본 정렬값과 같은 설정값을 원하는 데로 변경 할 수 있다는 점이다.

   ```python
   from django.db import models

   class Person(models.Model):
       first_name = models.CharField(max_length=30)
       last_name = models.CharField(max_length=30)

   class MyPerson(Person):
       class Meta:
           proxy = True

       def do_something(self):
           # ...
           pass
   ```

   ​







[^1]: null과 blank는 다르다. null은 존재가 하지않는다, blank는 0의 값이 들어간다.
[^2]: 객관식 문제.
[^3]: 별도로 지정하지 않는 한 id라는 IntergerField를 추가하여 `primary_key = True`를 준다. `models.AutoField(primary_key = True)`









































