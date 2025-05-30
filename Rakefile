require 'fileutils'

def remote_name
  ENV.fetch("REMOTE_NAME", "origin")
end

NSIS_VERSION = "3.11-1.el9"
PROJECT_ROOT = `git rev-parse --show-toplevel`.strip
BUILD_DIR    = File.join(PROJECT_ROOT, "build")
GH_PAGES_REF = File.join(BUILD_DIR, ".git/refs/remotes/#{remote_name}/gh-pages")

directory BUILD_DIR

file GH_PAGES_REF => BUILD_DIR do
  repo_url = nil

  cd PROJECT_ROOT do
    repo_url = `git config --get remote.#{remote_name}.url`.strip
  end

  cd BUILD_DIR do
    sh "git init"
    sh "git remote add #{remote_name} #{repo_url}"
    sh "git fetch #{remote_name}"
    sh "git checkout master"

    if `git branch -r` =~ /gh-pages/
      sh "git checkout gh-pages"
    else
      sh "git checkout --orphan gh-pages"
      sh "touch index.html"
      sh "git add ."
      sh "git commit -m 'initial gh-pages commit'"
      sh "git push #{remote_name} gh-pages"
    end
  end
end

# Alias to something meaningful
task :prepare_git_remote_in_build_dir => GH_PAGES_REF

# Fetch upstream changes on gh-pages branch
task :sync do
  cd BUILD_DIR do
    sh "git fetch #{remote_name}"
    sh "git reset --hard #{remote_name}/gh-pages"
  end
end

# Prevent accidental publishing before committing changes
task :not_dirty do
  puts "***#{ENV['ALLOW_DIRTY']}***"
  unless ENV['ALLOW_DIRTY']
    fail "Directory not clean" if /nothing to commit/ !~ `git status`
  end
end

desc "Compile all files into the build directory"
task :build do
  cd PROJECT_ROOT do
    sh %Q{rpmbuild -bb mingw-nsis.spec --define "_topdir #{PROJECT_ROOT}" --define "_rpmdir #{PROJECT_ROOT}" --define "_sourcedir #{PROJECT_ROOT}"}
    mkdir_p File.join(BUILD_DIR, 'rpms')
    cp "noarch/mingw32-nsis-#{NSIS_VERSION}.noarch.rpm", File.join(BUILD_DIR, 'rpms')
    cp "noarch/mingw64-nsis-#{NSIS_VERSION}.noarch.rpm", File.join(BUILD_DIR, 'rpms')
    cp "#{RbConfig::CONFIG['host_cpu']}/mingw-nsis-base-#{NSIS_VERSION}.#{RbConfig::CONFIG['host_cpu']}.rpm", File.join(BUILD_DIR, 'rpms')
  end

  cd BUILD_DIR do
    sh("repomanage --keep 3 --old rpm | xargs rm -fv")
    sh("createrepo --database --update . || createrepo --database .")
  end
end

desc "Build and publish to Github Pages"
task :publish => [:not_dirty, :prepare_git_remote_in_build_dir, :sync, :build] do
  message = nil
  suffix = ENV["COMMIT_MESSAGE_SUFFIX"]

  cd PROJECT_ROOT do
    head = `git log --pretty="%h" -n1`.strip
    message = ["Site updated to #{head}", suffix].compact.join("\n\n")
  end

  cd BUILD_DIR do
    sh 'git add --all'
    if /nothing to commit/ =~ `git status`
      puts "No changes to commit."
    else
      sh "git commit -m \"#{message}\""
    end
    sh "git push #{remote_name} gh-pages"
  end
end
