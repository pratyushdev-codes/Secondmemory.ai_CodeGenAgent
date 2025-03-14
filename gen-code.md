```java
public interface SoundMaker {
    String makeSound();
}

public class Dog implements SoundMaker {
    private String name;

    public Dog(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public String makeSound() {
        return "Woof!";
    }
}

public class Cat implements SoundMaker {
    private String name;

    public Cat(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public String makeSound() {
        return "Meow!";
    }
}

public class Bird implements SoundMaker {
    private String name;

    public Bird(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public String makeSound() {
        return "Tweet!";
    }
}

public class Main {
    public static void main(String[] args) {
        Dog myDog = new Dog("Buddy");
        Cat myCat = new Cat("Whiskers");
        Bird myBird = new Bird("Tweety");

        System.out.println(myDog.getName() + " says " + myDog.makeSound());
        System.out.println(myCat.getName() + " says " + myCat.makeSound());
        System.out.println(myBird.getName() + " says " + myBird.makeSound());
    }
}
```