require 'rubygems'
require 'mysql2'
require 'unsupervised-language-detection'


db1 = Mysql2::Client.new(:host => 'localhost', :username =>'cs2102', :password => '2012sc', :database => 'sgbeat')
db2 = Mysql2::Client.new(:host => 'localhost', :username =>'cs2102', :password => '2012sc', :database => 'sgb_pure')
tweets = db1.query("SELECT * FROM tweets").each do |row|
    str = row["tweet"]
    if UnsupervisedLanguageDetection.is_english_tweet?(str)
        str = db2.escape(str)
        db2.query("INSERT INTO tweets (tweet) VALUES ('#{str}')") 
    else
        puts "Not English: " + str
    end
end
db1.close
db2.close



