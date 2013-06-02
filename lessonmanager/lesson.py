from openerp.osv import osv
from openerp.osv import fields
from openerp import pooler

class lesson_category(osv.Model):
    _name = "lesson.category"

    _columns={
        "name":fields.char("Category Name",size=100,required=True,help="book category name"),
        "description":fields.char("Description",size=100)
    }
lesson_category()

class lesson_author(osv.Model):
    _name = "lesson.author"
    _columns={
        "name":fields.char("Author Name",size=100,required=True,help="Author name"),
        "age":fields.integer("Age",help="The age of this author"),
        "country":fields.many2one("res.country",string="Country Name"),
        "email":fields.char("Email",size=100),
        "address":fields.char("Address",size=200,attrs="{'readonly':[('name','=','tedi3231')]}"),
        "blog":fields.char("Blog Url",size=100,help="The blog's url of author"),
    }

    def author_blog_change(self,cr,uid,ids,blog):
        values = {}
        warning = {}
        if blog and not blog.lower().startswith('http://'):
            values['blog'] = 'http://' + blog
            #warning['title'] = 'blog'
            #warning['message'] = 'Url must be startswith http://'
            #warning['blog'] = 'url must be startswith http://'
        return {'value':values}

    def author_name_change(self,cr,uid,ids,name):
        v = {}
        print 'name=%s'%name
        if name:
            author = self.pool.get('lesson.author').browse(cr,uid,ids)
            print 'author type is %s'% type(author)
        v['name'] = 'tedi3231'
        return {'value':v}

lesson_author()

class lesson_book(osv.Model):
    _name="lesson.book"
    _columns={
        "name":fields.char("Book Name",size=60,required=True,help="Please input book name"),
        "category":fields.many2one("lesson.category",string="Book category"),
        "description":fields.char("Description",size=100),
    }
lesson_book()

class lesson_student(osv.Model):
    _name = "lesson.student"
    
    def _sel_country(self,cursor,user_id,context=None):
        country = self.pool.get("res.country")
        ids = country.search(cursor,user_id,[])
        res = country.read(cursor,user_id,ids,['name','code'],context)
        res = [(r['code'],r['name']) for r in res]
        return res

    _columns={
        "name":fields.char("Student Name",size=100,required=True,help="Input the name of student,include firstname and lastname"),
        "age":fields.integer("Age",required=True,help="The age of student"),
        "address":fields.char("Address",size=100,required=False,help="The address of student"),
        "status":fields.selection((('new','New'),('approve','Approve'),),"Status",required=True),
        "country":fields.selection(_sel_country,'Country',required=True)
    }
    _defaults = {
        'age':lambda *a:20,
        'status':lambda *a:'new',
    }
lesson_student()

class lesson_grade(osv.Model):
    _name= "lesson.grade"
    _columns={
        "name":fields.char("Grade Name", size=64),
        "courses":fields.many2one("lesson.course","Courses"),
    }
    
    def _check_name(self,cr,uid,ids,context={}):
        print 'ids=%s'%ids
        grades = [g.name for g in self.browse(cr,uid,ids)]
        print grades
        if not grades:
            return False
        current_grade = grades[0]
        print 'current_grade.name=%s'%current_grade
        result_ids = self.search(cr,uid,[('name','=',current_grade),('id','!=',ids[0])])

        print 'result_ids=%s'%result_ids
        if not result_ids:
            return True
        return False

    _constraints = [(_check_name,'Grade name has been exists!',['name'])]
    
lesson_grade()

class lesson_course(osv.Model):
    _name='lesson.course'
    _columns={
        'name':fields.char('Lesson Name',size=64),
        'description':fields.char('Description',size=100),
    }
lesson_course()


