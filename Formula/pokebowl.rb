class Pokebowl < Formula
  desc "Background runner for coding agents"
  homepage "https://github.com/TheLimeDev/PokeBowl"
  url "https://github.com/TheLimeDev/PokeBowl/releases/download/v0.1.0/pokebowl-0.1.0.tar.gz"
  sha256 "fb17696444259007a1a1735288b47b8606d14f4fb379884b22a584be4d271ff5"
  version "0.1.0"
  depends_on "python@3.12"

  def install
    libexec.install Dir["*"]
    (bin/"pokebowl").write <<~EOS
      #!/bin/bash
      exec "#{Formula["python@3.12"].opt_bin}/python3" "#{libexec}/pokebowl.py" "$@"
    EOS
  end

  test do
    system "#{bin}/pokebowl", "--version"
  end
end
